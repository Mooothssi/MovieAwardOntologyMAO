from datetime import date
from owlready2 import Ontology
from typing import List
from yaml import load, Loader


from .primitives import (BASE_ENTITIES, PROPERTY_ENTITIES,
                         OntologyEntity, OwlClass, OwlDataProperty,
                         OwlObjectProperty)

from .wrapper import BaseOntologyClass

DATATYPE_MAP = {
    'xsd:boolean': bool,
    'xsd:string': str,
    'xsd:integer': int,
    'xsd:decimal': float,
    'xsd:date': date
}


def create_owl_thing(name: str, onto: Ontology):
    return BaseOntologyClass(name=name, onto=onto)


def get_equivalent_datatype(entity_name: str):
    return DATATYPE_MAP.get(entity_name, entity_name)


class YamlToOwlConverter:
    imports = "from ontogen.wrapper import BaseOntologyClass\n\n\n"

    def __init__(self, spec_filename: str):
                 #ontology_filename: str = OWL_FILEPATH):
        # self.onto = get_ontology(f"file:////{ontology_filename}")
        # self.onto.load()
        self.entities = {}
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

                if base == OwlClass:
                    obj._internal_dict = sub
                    for prop in PROPERTY_ENTITIES:
                        if prop not in obj._internal_dict:
                            continue
                        prop_class = obj._internal_dict[prop]
                        for prop_name in prop_class:
                            prop_qualifier = f"{obj.prefix}:{prop_name}"
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_qualifier)
                            obj.parent_class_names = sub["rdfs:subClassOf"]
                    temp_classes.append(obj)

                self.entities[class_entity_name] = obj
        self._load_class_subclasses(temp_classes)

    def _load_class_subclasses(self, classes: List[OwlClass]):
        for cls in classes:
            [cls.add_superclass(self.get_entity(f"{cls.prefix}:{name}")) for name in cls.parent_class_names]

    def get_entity(self, entity_name: str) -> OntologyEntity or None:
        try:
            return self.entities[entity_name]
        except KeyError:
            return None

    def to_owl_ontology(self, onto: Ontology):
        for entity in self.entities.values():
            if isinstance(entity, OwlDataProperty):
                entity.instantiate(onto)
            elif isinstance(entity, OwlClass):
                entity.instantiate(onto)
