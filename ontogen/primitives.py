from owlready2 import (AllDisjoint, AnnotationProperty, DataProperty,
                       ObjectProperty, Thing)
from typing import Any, Dict, List, Type

from .base import Ontology, OntologyEntity, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME
from .internal import CHARACTERISTICS_MAPPING
from .wrapper import apply_classes_from
from .utils import ClassExpToConstruct

__all__ = ('OwlClass', 'OwlAnnotationProperty',
           'OwlDataProperty', 'OwlObjectProperty',
           'OwlThing', 'ENTITIES')

BUILTIN_DATA_TYPES = (str, int, float)
ENTITIES: Dict[str, OntologyEntity] = {}


def get_exp_constructor(onto: Ontology):
    return ClassExpToConstruct(onto)


def check_restrictions(prefix: str, str_types: List[str], value: Any) -> bool:
    t = type(value)
    # check for builtin types
    if t in BUILTIN_DATA_TYPES:
        return True
    p = set([f"{prefix}:{str_type}" for str_type in str_types]).intersection(ENTITIES.keys())
    return len(p) > 0


class OwlProperty(OntologyEntity):
    prefix = "owl"
    range = [Type[str]]

    # owlready-related implementation
    def actualize(self, onto: Ontology):
        """
        Instantiate a Property into a given Ontology

        :param individual_name: The name of an individual, creating an ontology Class if empty
        :param onto: An `owlready2` Ontology
        """
        if self.name in ["topObjectProperty", "topDataProperty"]:
            return
        apply_classes_from(onto)
        self._get_generated_class(onto, range=self.get_generated_range(onto))
        self._sync_internal(onto)

    def get_generated_range(self, onto: Ontology):
        return self.range


class OwlDataProperty(OwlProperty):
    name = "DataProperty"
    range = [str]
    _parent_class = DataProperty


class OwlAnnotationProperty(OwlProperty):
    name = "AnnotationProperty"
    range = [str]
    _parent_class = AnnotationProperty

    # owlready-related implementation
    def actualize(self, onto: Ontology):
        """
        Instantiate a Datatype Property into a given Ontology

        :param onto: An `owlready2` Ontology
        """
        self._get_generated_class(onto, range=self.range)


class OwlClass(OntologyEntity):
    """
        A class for ontology classes of instances
    """

    def __repr__(self) -> str:
        return f"OwlClass<{self.prefix}:{self.name}>"

    prefix = "owl"
    name = "Class"
    parent_name = "BaseOntologyClass"
    _parent_class = Thing
    parent_class_names: List[str] = []
    disjoint_class_names: List[str] = []

    def __init__(self, entity_name: str):
        super(OwlClass, self).__init__(entity_qualifier=entity_name)
        self.defined_properties: Dict[str, "OwlProperty" or None] = dict(ENTITIES)

    # owlready-related implementation
    def instantiate(self, onto: Ontology, individual_name: str):
        """
        Instantiate Individuals into a given Ontology

        :param individual_name: The name of an individual, creating an ontology Class if empty
        :param onto: An `owlready2` Ontology
        """
        if not self.is_actualized:
            self.actualize(onto)
        apply_classes_from(onto)
        self._sync_internal(onto)
        inst = self._get_generated_class(onto)()
        inst.name = individual_name
        self._internal_imp_instance = inst

    def actualize(self, onto: Ontology) -> 'OwlClass':
        """
        Makes the entity concrete (saved) in a given Ontology

        Args:
            onto: a given Ontology
        """
        apply_classes_from(onto)
        [self.add_equivalent_class_expression(get_exp_constructor(onto).to_construct(exp))
         for exp in self.equivalent_class_expressions]
        self._sync_internal(onto)
        self._get_generated_class(onto)
        disj = [x._get_generated_class(onto) for x in self._disjoint_classes if x is not None]
        if len(disj) > 0:
            AllDisjoint(disj)
        return self

    def add_property_assertion(self, property_name: str, value):
        """
            Adds property assertions with values
        """
        assert self.is_individual, \
            "Must be an Individual before adding any assertion. Please call instantiate() first"
        assert ":" in property_name and len(property_name.split(":")) == 2, "Please add prefix"
        self.properties_values[property_name] = value
        assert property_name in self.defined_properties, \
            "Must associate a subclass of OwlProperty with the given name before any assertion can be done"
        self._assert_restrictions(self.defined_properties[property_name].range, value)

    def _assert_restrictions(self, types: List[str], value):
        assert check_restrictions(self.prefix, types, value), \
            "The added value doesn't match the range restriction!"


class OwlThing(OwlClass):
    name = "Thing"
    parent_name = "BaseOwlThing"
    prefix = "owl"
    _internal_imp_instance = Thing

    def __init__(self):
        super().__init__(f"{self.prefix}:{self.name}")

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        return self._internal_imp_instance


class OwlObjectProperty(OwlProperty):
    name = "ObjectProperty"
    _range = [OwlClass("owl:Thing")]
    _parent_class = ObjectProperty
    _characteristics = ["owl:SymmetricProperty"]

    def __init__(self, name: str):
        super().__init__(name)
        self._realised_parent_classes.append(ObjectProperty)
        self.inverse_prop: Type or None = None

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        u = [CHARACTERISTICS_MAPPING.get(c, None) for c in self._characteristics]
        if self.inverse_prop is not None:
            attrs['inverse_property'] = self.get_generated_inverse(onto)
        if len(u) > 0:
            self._realised_parent_classes.extend(u)
        return super(OwlObjectProperty, self)._get_generated_class(onto, **attrs)

    def get_generated_range(self, onto: Ontology):
        return [x._get_generated_class(onto) for x in self.range if x is not None]

    def get_generated_inverse(self, onto: Ontology) -> Type:
        self.inverse_prop.inverse_prop = None
        return self.inverse_prop._get_generated_class(onto)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, a):
        self._range = a
        self.dependencies.extend([b for b in a if not b == "Thing" and b != ""])


BASE_ENTITIES = [OwlAnnotationProperty, OwlDataProperty, OwlObjectProperty, OwlClass]
PROPERTY_ENTITIES = {"annotations": OwlAnnotationProperty,
                     "dataProperty": OwlDataProperty,
                     "objectProperty": OwlObjectProperty}
BUILTIN_ENTITIES = {
    LABEL_ENTITY_NAME: OwlAnnotationProperty(LABEL_ENTITY_NAME),
    COMMENT_ENTITY_NAME: OwlAnnotationProperty(COMMENT_ENTITY_NAME)
}
