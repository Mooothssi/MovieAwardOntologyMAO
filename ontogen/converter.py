from owlready2 import Ontology
from typing import Tuple
from yaml import load, Loader


from .base import DATATYPE_MAP
from .primitives import (BASE_ENTITIES, COMMENT_ENTITY_NAME, ENTITIES,
                         LABEL_ENTITY_NAME, PROPERTY_ENTITIES,
                         OntologyEntity, OwlClass, OwlDataProperty,
                         OwlObjectProperty)
from .wrapper import BaseOntologyClass


def create_owl_thing(name: str, onto: Ontology):
    return BaseOntologyClass(name=name, onto=onto)


def get_equivalent_datatype(entity_name: str):
    return DATATYPE_MAP.get(entity_name, entity_name)


class YamlToOwlConverter:
    def __init__(self, spec_filename: str):
        self.entities = ENTITIES
        self.spec_filename = spec_filename
        self._load_file()

    def _load_file(self):
        dct = load(open(self.spec_filename), Loader=Loader)
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
                        if "rdfs:range" in sub:
                            obj.range = sub["rdfs:range"]
                    elif base == OwlDataProperty:
                        if "rdfs:range" in sub:
                            obj.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]
                    annotations = sub["annotations"]
                    obj.add_label(annotations.get(LABEL_ENTITY_NAME, [None])[0])
                    obj.add_comment(annotations.get(COMMENT_ENTITY_NAME, [None])[0])
                if base == OwlClass:
                    obj._internal_dict = sub
                    for prop in PROPERTY_ENTITIES:
                        if prop not in obj._internal_dict:
                            continue
                        prop_class = obj._internal_dict[prop]
                        obj.parent_class_names = sub.get("rdfs:subClassOf", [])
                        obj.disjoint_class_names = sub.get("owl:disjointWith", [])
                        for prop_name in prop_class:

                            prop_qualifier = f"{obj.prefix}:{prop_name}"
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_qualifier)
                    temp_classes.append(obj)
                self.entities[class_entity_name] = obj
        self._load_class_descriptions(tuple(self.entities.values()))

    def _load_class_descriptions(self, classes: Tuple[OntologyEntity]):
        for cls in classes:
            if isinstance(cls, OwlClass):
                [cls.add_superclass(self.get_entity(f"{cls.prefix}:{name}")) for name in cls.parent_class_names]
                [cls.add_disjoint_classes(self.get_entity(f"{cls.prefix}:{name}")) for name in cls.disjoint_class_names]
            elif isinstance(cls, OwlObjectProperty):
                cls.range = [self.get_entity(f"{cls.prefix}:{name}") for name in cls.range]

    def get_entity(self, entity_name: str) -> OntologyEntity or None:
        try:
            return self.entities[entity_name]
        except KeyError:
            return None

    def to_owl_ontology(self, onto: Ontology):
        for entity in self.entities.values():
            entity.instantiate(onto)
