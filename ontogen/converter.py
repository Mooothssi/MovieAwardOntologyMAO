from typing import Tuple
from yaml import load, Loader


from .base import DATATYPE_MAP
from .primitives import (BASE_ENTITIES, COMMENT_ENTITY_NAME, ENTITIES,
                         LABEL_ENTITY_NAME, PROPERTY_ENTITIES, Ontology,
                         OntologyEntity, OwlClass, OwlDataProperty, OwlThing,
                         OwlObjectProperty)
from .wrapper import BaseOntologyClass
from .utils import ClassExpToConstruct


def create_owl_thing(name: str, onto: Ontology):
    return BaseOntologyClass(name=name, onto=onto)


def get_equivalent_datatype(entity_name: str):
    return DATATYPE_MAP.get(entity_name, entity_name)


def get_qualified_entity(name: str, fallback_prefix: str = "mao"):
    return name if ":" in name else f"{fallback_prefix}:{name}"


class YamlToOwlConverter:
    """
        A converter from YAML to an abstraction of OWL ontology
    """
    def __init__(self, spec_filename: str):
        """
        Loads a file with the given name into a skeleton of an OWL ontology.
        Needs to be actualized by `Ontology` class.

        Args:
            spec_filename: The filename of a YAML spec file
        """
        self.entities = ENTITIES
        self.spec_filename = spec_filename
        self.class_exp_constructor = ClassExpToConstruct()
        self._load_file()

    def _load_file(self):
        with open(self.spec_filename) as f:
            dct = load(f, Loader=Loader)
        temp_classes = []
        for base in BASE_ENTITIES:
            cls = base
            q = base.get_entity_name()
            if q not in dct:
                continue
            classes = dct[q]
            for class_entity_name in classes:
                if class_entity_name == "owl:Thing":
                    continue
                obj = cls(class_entity_name)
                sub = classes[class_entity_name]
                if isinstance(sub, dict):
                    if base == OwlObjectProperty:
                        obj._characteristics = sub.get("rdf:type", [])
                        obj.range = sub.get("rdfs:range", [])
                        inv = sub.get("owl:inverseOf", [])
                        if len(inv) == 1:
                            obj.inverse_prop = inv[0]
                    elif base == OwlDataProperty:
                        if "rdfs:range" in sub:
                            obj.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]
                    annotations = sub["annotations"]
                    obj.add_labels(annotations.get(LABEL_ENTITY_NAME, [None]))
                    obj.add_comments(annotations.get(COMMENT_ENTITY_NAME, [None]))
                if base == OwlClass:
                    obj._internal_dict = sub
                    for prop in PROPERTY_ENTITIES:
                        if prop not in obj._internal_dict:
                            continue
                        prop_class = obj._internal_dict[prop]
                        obj.parent_class_names = sub.get("rdfs:subClassOf", [])
                        obj.disjoint_class_names = sub.get("owl:disjointWith", [])
                        obj.equivalent_class_expressions = sub.get("rdfs:equivalentClass", [])
                        for prop_name in prop_class:
                            prop_qualifier = get_qualified_entity(prop_name)
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_name)
                    temp_classes.append(obj)
                self.entities[class_entity_name] = obj
        self._load_class_descriptions(tuple(self.entities.values()))

    def _load_class_descriptions(self, classes: Tuple[OntologyEntity]):
        for cls in classes:
            if isinstance(cls, OwlClass) or isinstance(cls, OwlObjectProperty):
                [cls.add_superclass(self.get_entity(name, cls.prefix)) for name in cls.parent_class_names]
                if isinstance(cls, OwlClass):
                    [cls.add_disjoint_classes(self.get_entity(name, cls.prefix)) for name in cls.disjoint_class_names]
                elif isinstance(cls, OwlObjectProperty):
                    cls.range = [self.get_entity(name, cls.prefix) for name in cls.range]
                    cls.inverse_prop = self.get_entity(cls.inverse_prop, cls.prefix)

    def get_entity(self, entity_name: str, fallback_prefix: str = "mao") -> OntologyEntity or None:
        if entity_name is None:
            return None
        entity_name = get_qualified_entity(entity_name, fallback_prefix)
        if entity_name == "owl:Thing" or entity_name == "mao:Thing":
            return OwlThing()
        try:
            return self.entities[entity_name]
        except KeyError:
            return None

    def to_owl_ontology(self, onto: Ontology):
        """
            Saves changes made into a given Ontology
            :param onto: A given Ontology
        """
        for entity in self.entities.values():
            entity.actualize(onto)

