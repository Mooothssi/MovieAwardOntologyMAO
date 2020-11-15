from owlready2 import Ontology, Thing, ThingClass
from typing import Type, Dict


class BaseOntologyClass(Thing):
    def __init__(self, name: str, onto: Ontology = None):
        if onto is not None:
            self.namespace = onto
            self.ontology = onto
        super().__init__(name)

    @property
    def instances(self):
        return self.ontology_class.instances()

    @property
    def _ontology_class(self) -> ThingClass:
        return getattr(self.ontology, self.__class__.__name__)

    # def __setattr__(self, key, value):
    #     att = getattr(self, key)
    #     if isinstance(att, list):
    #         att += value
    #     else:
    #         new_value = [value]  # owlready2 implementation
    #         super().__setattr__(key, new_value)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]).union([cls])


def apply_classes_from(onto: Ontology):
    for s in all_subclasses(BaseOntologyClass):
        s.namespace = onto
        setattr(s, 'storid', onto.world._abbreviate(s.iri))


class OntologyEntity:
    prefix = "owl"
    name = "any"
    _internal_dict = {}

    def __init__(self, entity_qualifier: str):
        pre, n = entity_qualifier.split(":")
        self.prefix = pre
        self.name = n
        self.dependencies = []

    @classmethod
    def get_entity_qualifier(cls) -> str:
        return f"{cls.prefix}:{cls.name}"


class OwlClass(OntologyEntity):
    prefix = "owl"
    name = "Class"
    properties = []
    parent_name = "BaseOntologyClass"

    def __init__(self, entity_qualifier: str):
        super(OwlClass, self).__init__(entity_qualifier=entity_qualifier)
        self.properties = []
    
    def __str__(self):
        property_dump = "\n"
        for prop in self.properties:
            property_dump += f"    {prop}\n"
        else:
            property_dump += "    pass"
        return f"class {self.name}({self.parent_name}):" \
               f"{property_dump}"


class OwlThing(OwlClass):
    name = "Thing"
    parent_name = "BaseOwlThing"


class OwlProperty(OntologyEntity):
    prefix = "owl"
    range = ["xsd:string"]


class OwlDataProperty(OwlProperty):
    name = "DataProperty"
    range = ["xsd:string"]


class OwlObjectProperty(OwlProperty):
    name = "ObjectProperty"
    _range = ["owl:Class"]

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, a):
        self._range = a
        self.dependencies.extend([b for b in a if not b == "Thing" and b != ""])

    def __str__(self):
        str_obj = f"{self.name}" if len(self.range) > 0 or self.name == "ObjectProperty" else "<unk>"
        if "owl:Class" not in self.range:
            str_obj += f": {self.range[0]}"
        else:
            str_obj += f": Thing"
        return str_obj


class OwlAnnotationProperty(OwlProperty):
    name = "AnnotationProperty"
    range = ["rdfs:label"]


BASE_ENTITIES = [OwlAnnotationProperty, OwlDataProperty, OwlObjectProperty, OwlClass]
PROPERTY_ENTITIES = {# "annotations": OwlAnnotationProperty,
                     "dataProperty": OwlDataProperty,
                     "objectProperty": OwlObjectProperty}
ENTITIES: Dict[str, OntologyEntity] = {}


def get_match(identifier: str) -> Type[OntologyEntity]:
    for entity in BASE_ENTITIES:
        if identifier == entity.get_entity_qualifier():
            return entity
