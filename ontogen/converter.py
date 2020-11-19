from typing import Dict, Tuple
from yaml import load, Loader
from semver import VersionInfo

from .base import DATATYPE_MAP
from .base.namespaces import OWL_CLASS, OWL_EQUIVALENT_CLASS, OWL_RESTRICTION
import ontogen.primitives as primitives
from .primitives import (BASE_ENTITIES, COMMENT_ENTITY_NAME,
                         LABEL_ENTITY_NAME, PROPERTY_ENTITIES, Ontology,
                         OntologyEntity, OwlClass, OwlDataProperty, OwlThing,
                         OwlObjectProperty)


def get_equivalent_datatype(entity_name: str):
    return DATATYPE_MAP.get(entity_name, entity_name)


def get_qualified_entity(name: str, fallback_prefix: str = "mao"):
    return name if ":" in name else f"{fallback_prefix}:{name}"


class YamlToOwlConverter:
    """
        A converter from YAML to an abstraction of OWL ontology
    """
    SUPPORTED_VERSION = "1.1.0"

    def __init__(self, spec_filename: str, base_prefix: str="mao"):
        """
        Loads a file with the given name into a skeleton of an OWL ontology.
        Needs to be actualized by `Ontology` class.

        Args:
            spec_filename: The filename of a YAML spec file
        """
        self.entities: Dict[str, OntologyEntity] = {}
        self.spec_filename = spec_filename
        self.prefix = base_prefix
        self.ontology = Ontology(base_prefix=base_prefix)
        self.ontology.name_from_prefix()
        self.ontology.create()
        self.file_version = ""
        self._missing_entities = set()
        self._load_file()

    def _check_eligible_version(self, base_dict: dict):
        self.file_version = base_dict["version"].replace("v", "")
        assert VersionInfo.parse(self.file_version)\
            .compare(VersionInfo.parse(YamlToOwlConverter.SUPPORTED_VERSION)) <= 0, "Unsupported version of file"

    def _load_file(self):
        with open(self.spec_filename) as f:
            dct = load(f, Loader=Loader)
            self._check_eligible_version(dct)
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
                e = get_qualified_entity(class_entity_name, self.prefix)
                prefix, name = e.split(":")
                obj = cls(e)
                obj.prefix = prefix
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
                    annotations = sub.get("annotations", {})
                    obj.add_labels(annotations.get(LABEL_ENTITY_NAME, [None]))
                    obj.add_comments(annotations.get(COMMENT_ENTITY_NAME, [None]))
                if base == OwlClass:
                    obj._internal_dict = sub
                    obj.parent_class_names = sub.get("rdfs:subClassOf", [])
                    obj.disjoint_class_names = sub.get("owl:disjointWith", [])
                    obj.equivalent_class_expressions = self._get_equivalent_classes(sub)
                    for prop in PROPERTY_ENTITIES:
                        if prop not in sub:
                            continue
                        prop_class = sub[prop]
                        for prop_name in prop_class:
                            prop_qualifier = get_qualified_entity(prop_name)
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_name)
                    temp_classes.append(obj)
                self.entities[class_entity_name] = obj
        if "annotations" in dct:
            anno = dct["annotations"]
            self.ontology.add_label(anno["rdfs:label"][0])
            self.ontology.add_annotation("licence", anno["dcterms:licence"][0])
            self.ontology.add_annotation("title", anno["dc:title"][0])
        self._load_class_descriptions(tuple(self.entities.values()))
        primitives.ENTITIES = self.entities

    @staticmethod
    def _get_equivalent_classes(sub_dict: dict):
        if OWL_EQUIVALENT_CLASS not in sub_dict:
            return []
        u = sub_dict[OWL_EQUIVALENT_CLASS]
        if isinstance(u, dict):
            return u.get(OWL_RESTRICTION, [])
        else:
            return u

    def _load_class_descriptions(self, classes: Tuple[OntologyEntity]):
        for cls in classes:
            if isinstance(cls, OwlClass) or isinstance(cls, OwlObjectProperty):
                [cls.add_superclass(self.get_entity(name, cls.prefix)) for name in cls.parent_class_names]
                if isinstance(cls, OwlClass):
                    [cls.add_disjoint_class(self.get_entity(name, cls.prefix)) for name in cls.disjoint_class_names]
                elif isinstance(cls, OwlObjectProperty):
                    cls.range = [self.get_entity(name, cls.prefix) for name in cls.range if isinstance(name, str)]
                    cls.inverse_prop = self.get_entity(cls.inverse_prop)

    def get_entity(self, entity_name: str, prefix: str = None) -> OwlClass or OntologyEntity or str:
        if entity_name is None:
            return None
        if prefix is None:
            prefix = self.prefix
        modified_name = get_qualified_entity(entity_name, prefix)
        if modified_name == "owl:Thing" or modified_name == f"{prefix}:Thing":
            return None
        try:
            if modified_name in self._missing_entities:
                self._missing_entities.remove(modified_name)
            return self.entities[modified_name]
        except KeyError:
            self._missing_entities.add(modified_name)
            return modified_name

    def check_missing_definitions(self):
        if len(self._missing_entities) > 0:
            missing = "\n".join([f"- {e}" for e in self._missing_entities])
            raise AssertionError(f"There are missing entities as follows. "
                                 f"Please check the consistency of the given specs!\n{missing}")

    def list_entities(self):
        """
        Print out list of entities to the console
        """
        for entity in self.entities:
            print(f"- {entity}: {self.entities[entity].__class__.__name__}")

    def export_to_ontology(self, onto: Ontology = None) -> Ontology:
        """
            Saves changes made into a given Ontology
            :param onto: A given Ontology
        """
        self.check_missing_definitions()
        if onto is None:
            onto = self.ontology
            onto.name_from_prefix()
        onto.create()
        self.prefix = onto.implementation.name
        for entity in self.entities.values():
            entity.actualize(onto)
        onto.actualize()
        return onto
