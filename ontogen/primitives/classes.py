from typing import List, Dict, Type

from owlready2 import Thing, AllDisjoint

from ontogen.base import OwlActualizable
from ontogen.base.vars import GENERATED_TYPES
from .base import OwlEntity, Ontology, ENTITIES, apply_classes_from, get_exp_constructor, check_restrictions, \
    absolutize_entity_name
from ..base.assertable import OwlAssertable


class OwlClass(OwlEntity):
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
        self.individuals: List[OwlIndividual] = []
        self.defined_properties: Dict[str, "OwlProperty" or None] = dict(ENTITIES)

    def actualize(self, onto: Ontology) -> 'OwlClass':
        """
        Makes the entity concrete (saved) in a given Ontology

        Args:
            onto: a given Ontology
        """
        apply_classes_from(onto)
        for i in self.individuals:
            i.actualize_imp(onto)
        [self.add_equivalent_class_expression(get_exp_constructor(onto).to_construct(exp))
         for exp in self.equivalent_class_expressions]
        for idx, x in enumerate(self._parent_classes):
            if isinstance(x, str):
                c = get_exp_constructor(onto).to_construct(x)
                self._parent_classes[idx] = c
        inst = self._get_generated_class(onto)
        self.actualize_assertions(inst)
        for i in self.individuals:
            i.actualize_imp(onto)
        disjoints = [x._get_generated_class(onto) for x in self._disjoint_classes if x is not None]
        if len(disjoints) > 0:
            AllDisjoint(disjoints)
        return self


class OwlThing(OwlClass):
    name = "Thing"
    parent_name = "BaseOwlThing"
    prefix = "owl"
    _internal_imp_instance = Thing

    def __init__(self):
        super().__init__(f"{self.prefix}:{self.name}")

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        return self._internal_imp_instance


class OwlIndividual(OwlActualizable, OwlAssertable):
    """
    An Individual of Ontology classes
    """
    def __init__(self, name: str):
        self.name = name
        self.onto_types: List[OwlClass] = []
        self.defined_properties: Dict[str, "OwlProperty" or None] = dict(ENTITIES)
        self._imp = None
        self.properties_values: Dict[str, ] = {}
        self.prefix = self.name.split(":")[0]

    def be_type_of(self, cls: OwlClass):
        """
        Sets the type of this Individual to be of a given Class

        Args:
            cls: A given Class
        """
        cls.individuals.append(self)
        self.onto_types.append(cls)

    def actualize(self, onto: Ontology):
        self.onto_types[0].actualize(onto)

    def _get_entity(self, onto: Ontology, relative_name: str) -> object or None:
        name = absolutize_entity_name(relative_name)
        return onto.entities.get(name, None)

    def actualize_imp(self, onto: Ontology):
        name = self.name.split(":")[1]
        try:
            if self._imp:
                inst = GENERATED_TYPES[name]
            else:
                inst = self.onto_types[0].actualized_entity()
            inst.name = name
            [y.actualize(onto) for y in [self._get_entity(onto, prop) for prop in self.properties_values] if y]
            GENERATED_TYPES[inst.name] = inst
            self.actualize_assertions(inst)
            self._imp = inst
        except AssertionError:
            pass

    def add_property_assertion(self, property_name: str, value):
        """
            Adds a property assertion with a given value
        """
        # assert self._imp, \
        #     "Must be an Individual before adding any assertion. Please call instantiate() first"
        assert ":" in property_name and len(property_name.split(":")) == 2, "Please add prefix"
        self.properties_values[property_name] = value
        # assert property_name in self.defined_properties, \
        #     "Must associate a subclass of OwlProperty with the given name before any assertion can be done"
        # self._assert_restrictions(self.defined_properties[property_name].range, value)

    def _assert_restrictions(self, types: List[str], value):
        assert check_restrictions(self.prefix, types, value), \
            "The added value doesn't match the range restriction!"

