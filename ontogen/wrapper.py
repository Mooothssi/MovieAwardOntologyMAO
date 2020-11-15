from owlready2 import Ontology, Thing, ThingClass
from typing import (Any, Dict, List, Type)


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
    for s in all_subclasses(Thing):
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


TYPE_MAPPING = {
    str: 'xsd:string',
    int: 'xsd:integer',
}


def check_restrictions(prefix: str, str_types: List[str], value: Any) -> bool:
    t = type(value)
    p = {}
    # check for builtin types
    if t in TYPE_MAPPING:
        p = set(str_types).intersection([TYPE_MAPPING[t]])
        if len(p) == 0:
            # check in defined classes
            p = set(str_types).intersection(ENTITIES.keys())
    return len(p) > 0


GENERATED_TYPES = {}


class OwlClass(OntologyEntity):
    """
        A class for ontology classes of instances
    """
    prefix = "owl"
    name = "Class"
    properties_values = {}
    parent_name = "BaseOntologyClass"
    # Short for an Implementation instance
    _internal_imp_instance: BaseOntologyClass = None

    def __init__(self, entity_qualifier: str):
        super(OwlClass, self).__init__(entity_qualifier=entity_qualifier)
        self.defined_properties: Dict[str, "OwlProperty"] = {}
    
    def __str__(self):
        property_dump = "\n"
        for prop in self.defined_properties:
            property_dump += f"    {prop}\n"
        else:
            property_dump += "    pass"
        return f"class {self.name}({self.parent_name}):" \
               f"{property_dump}"

    @property
    def is_instance(self) -> bool:
        return self._internal_imp_instance is not None

    def get_generated_class(self, onto: Ontology) -> type:
        if self.name in GENERATED_TYPES:
            return GENERATED_TYPES[self.name]
        GENERATED_TYPES[self.name] = type(self.name, (Thing,), {'namespace': onto})
        return GENERATED_TYPES[self.name]

    # owlready-related implementation
    def instantiate(self, onto: Ontology, individual_name: str = ""):
        """
        Instantiate Individuals into a given Ontology

        :param individual_name: The name of an individual, creating an ontology Class if empty
        :param onto: An `owlready2` Ontology
        """
        apply_classes_from(onto)
        indiv_name = self.name if individual_name == "" else individual_name
        if indiv_name == self.name:
            self.get_generated_class(onto)
        else:
            inst = self.get_generated_class(onto)()
            inst.name = indiv_name
            self._internal_imp_instance = inst

    def _sync_internal(self):
        if not self.is_instance:
            return
        inst = self._internal_imp_instance
        for set_prop in self.properties_values:
            val = self.properties_values[set_prop]
            set_prop = set_prop.split(":")[1]
            if isinstance(val, list):
                setattr(inst, set_prop, val)
            else:
                setattr(inst, set_prop, [val])

    def add_property_assertion(self, property_name: str, value):
        """
            Adds property assertions with values
        """
        assert ":" in property_name and len(property_name.split(":")) == 2, "Please add prefix"
        self.properties_values[property_name] = value
        assert check_restrictions(self.prefix, self.defined_properties[property_name].range, value), \
            "The value added doesn't match the range restriction!"
        self._sync_internal()


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
