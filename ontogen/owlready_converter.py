import os
from pathlib import Path
from owlready2 import Ontology, get_ontology
from yaml import load, Loader

from ontogen.wrapper import BASE_ENTITIES, PROPERTY_ENTITIES, get_match
from settings import OWL_FILEPATH
from .wrapper import BaseOntologyClass, OwlClass, OwlObjectProperty, OntologyEntity, apply_classes_from


def create_owl_thing(name: str, onto: Ontology):
    return BaseOntologyClass(name=name, onto=onto)


class YamlToOwlConverter:
    imports = "from ontogen.wrapper import BaseOntologyClass\n\n\n"

    def __init__(self,
                 spec_filename: str):
                 #ontology_filename: str = OWL_FILEPATH):
        # self.onto = get_ontology(f"file:////{ontology_filename}")
        # self.onto.load()
        self.entities = {}
        self.spec_filename = spec_filename
        self._load_file()

    def _load_file(self):
        dct = load(open(self.spec_filename), Loader=Loader)

        for base in BASE_ENTITIES:
            cls = base
            q = base.get_entity_qualifier()
            if q not in dct:
                continue
            classes = dct[q]
            for class_entity_name in classes:

                if class_entity_name == "owl:Thing":
                    continue
                obj = cls(class_entity_name)
                if base == OwlObjectProperty:
                    sub = classes[class_entity_name]
                    if isinstance(sub, dict):
                        if "rdfs:range" in sub:
                            obj.range = sub["rdfs:range"]

                elif base == OwlClass:
                    obj._internal_dict = classes[class_entity_name]
                    for prop in PROPERTY_ENTITIES:
                        if prop not in obj._internal_dict:
                            continue
                        prop_class = obj._internal_dict[prop]
                        for prop_name in prop_class:
                            prop_qualifier = f"{obj.prefix}:{prop_name}"
                            obj.defined_properties[prop_qualifier] = self.get_entity(prop_qualifier)
                self.entities[class_entity_name] = obj

    def get_entity(self, entity_qualifier: str) -> OntologyEntity or None:
        try:
            return self.entities[entity_qualifier]
        except KeyError:
            return None

    # def convert(self):
    #     self.sync_with_ontology()
    #     for entity in self.entities:
    #         if isinstance(entity, OwlClass):
    #             create_owl_thing(entity.name, self.onto)

    def to_python_scripts(self, base_path: str):
        for entity in self.entities.values():
            if isinstance(entity, OwlClass):
                classname = entity.name
                dep_str = ""
                d = ', '.join([', '.join(p.dependencies) for p in entity.defined_properties])
                if d.strip() != "":
                    dep_str = f"from . import {d.strip(', ').replace(', , ',', ')}\n\n\n"
                class_dump = f"{self.imports}"\
                             f"{dep_str}"\
                             f"{entity}"
                class_filename = f"{classname}.py"
                out_path = Path(base_path) / "generated" / entity.prefix
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                print(class_dump, file=open(out_path / class_filename, "w"))

    def to_owl_ontology(self, onto: Ontology):
        for entity in self.entities.values():
            if isinstance(entity, OwlClass):
                entity.instantiate(onto)

    # def sync_with_ontology(self):
    #     apply_classes_from(self.onto)
