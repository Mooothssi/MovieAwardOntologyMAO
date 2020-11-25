from typing import Type, Union, List

from owlready2 import (AnnotationProperty, DataProperty, ObjectProperty, Thing, AllDisjoint, destroy_entity)

from ontogen import OwlClass, OwlObjectProperty, OwlIndividual
from ontogen.actualizers.base import OntologyActualizer, OntologyBaseActualizer
from ontogen.actualizers.types import ACTUALIZED_CLASS
from ontogen.base import OwlEntity, GENERATED_TYPES
from ontogen.base.ontology import Ontology
from ontogen.internal import CHARACTERISTICS_MAPPING
from ontogen.primitives.base import OwlProperty, OwlAnnotationProperty, OwlDataProperty
from ontogen.utils.classexp import ClassExpToConstruct

TYPE_MAPPING = {
    OwlAnnotationProperty: AnnotationProperty,
    OwlObjectProperty: ObjectProperty,
    OwlDataProperty: DataProperty,
    OwlClass: Thing
}


def cleanup(onto: Ontology):
    onto.implementation.graph.destroy()
    for e in GENERATED_TYPES:
        destroy_entity(GENERATED_TYPES[e])
    GENERATED_TYPES.clear()


def get_exp_constructor(onto: Ontology):
    return ClassExpToConstruct(onto)
# GENERATED_TYPES: Dict[str, Union[Type[Thing], Thing, type]] = {}


class OwlreadyBaseActualizer(OntologyBaseActualizer):
    def get_actualized_entity(self, cls: OwlEntity, onto: Ontology, **attrs) -> Type[Thing]:
        """Returns an actualized Class of the given Ontology

        Args:
            cls:
            onto:
            **attrs: ``owlready`` attributes

        Returns:
            An actualized Class
        """
        try:
            cls._sync_description()
            return cls.actualized_entity
        except AssertionError:
            attrs['namespace'] = onto.implementation
            default = True
            if len(cls._parent_classes) > 0 or len(cls._realised_parent_classes) > 0:
                cls._realised_parent_classes.extend(
                    [self.get_actualized_entity(x, onto) for x in cls._parent_classes
                     if x is not None and isinstance(x, OwlEntity)])
                gen = cls._realised_parent_classes
                if len(gen) > 0:
                    GENERATED_TYPES[cls.name] = type(cls.name, tuple(gen), attrs)
                    default = False
            if default:
                GENERATED_TYPES[cls.name] = type(cls.name, (TYPE_MAPPING[cls.__class__],), attrs)
            if onto.base_prefix != cls.prefix:
                p = cls.get_iri(onto)
                cls.actualized_entity.iri = p
            cls.actualize_assertions(GENERATED_TYPES[cls.name])
            cls._actualized_entity = GENERATED_TYPES[cls.name]
            cls._sync_description()
            return GENERATED_TYPES[cls.name]


class OwlreadyClassActualizer(OwlreadyBaseActualizer):
    onto: Ontology
    base_parent_class: Thing = Thing

    def actualize(self, cls: OwlClass, onto: Ontology) -> 'OwlClass':
        """Makes the entity concrete (saved) in a given Ontology

        Args:
            onto: a given Ontology
        """
        super().actualize(cls, onto)
        for i in cls.individuals:
            self.actualize_individual(i, onto)
        [cls.add_equivalent_class_expression(get_exp_constructor(onto).to_construct(exp))
         for exp in cls.equivalent_class_expressions]
        for idx, x in enumerate(cls._parent_classes):
            if isinstance(x, str):
                c = get_exp_constructor(onto).to_construct(x)
                cls._parent_classes[idx] = c
        generated_cls = self.get_actualized_entity(cls, onto)
        cls.actualize_assertions(generated_cls)
        for i in cls.individuals:
            self.actualize_individual(i, onto)
        disjoints = [self.get_actualized_entity(x, onto) for x in cls._disjoint_classes if x is not None]
        if len(disjoints) > 0:
            AllDisjoint(disjoints)
        return cls

    def actualize_individual(self, cls: OwlIndividual, onto: Ontology):
        res = cls.name_with_prefix.split(":")
        assert len(res) > 1, "Must include a prefix"
        name = res[1]
        try:
            if cls._imp:
                inst = GENERATED_TYPES[name]
            else:
                inst = cls.onto_types[0].actualized_entity()
            inst.name = name
            [self.actualize(y, onto) for y in [onto.get_entity(onto, prop) for prop in cls.properties_values] if y]
            GENERATED_TYPES[inst.name] = inst
            cls.actualize_assertions(inst)
            cls._imp = inst
        except AssertionError:
            pass


class OwlreadyPropertyActualizer(OwlreadyBaseActualizer):
    def actualize(self, cls: OwlProperty, onto: Ontology):
        if isinstance(cls, OwlAnnotationProperty):
            self.get_actualized_entity(cls, onto, range=cls.range)
        else:

            if cls.name in ["topObjectProperty", "topDataProperty"]:
                return
            super().actualize(cls, onto)
            p = self.get_actualized_entity(cls, onto)
            cls.actualize_assertions(p)

    def _get_generated(self, cls: OwlEntity, onto: Ontology, classes: List[OwlEntity]) -> List[ACTUALIZED_CLASS]:
        if isinstance(cls, OwlObjectProperty):
            return [super(OwlreadyPropertyActualizer, self).get_actualized_entity(x, onto)
                    for x in classes if x is not None]
        else:
            lst = []
            for c in classes:
                if isinstance(c, OwlEntity):
                    c = super().get_actualized_entity(c, onto)
                lst.append(c)
            return lst

    def get_actualized_entity(self, cls: Union[OwlObjectProperty, OwlProperty], onto: Ontology, **attrs) -> Type[Thing]:
        if isinstance(cls, OwlProperty):
            attrs['domain'] = self._get_generated(cls, onto, cls.domain)
            attrs['range'] = self._get_generated(cls, onto, cls.range)
        if isinstance(cls, OwlObjectProperty):
            cls._realised_parent_classes.append(ObjectProperty)
            u = [CHARACTERISTICS_MAPPING.get(c, None) for c in cls._characteristics]
            if cls.inverse_prop is not None:
                attrs['inverse_property'] = self.get_generated_inverse(cls, onto)
            if len(u) > 0:
                cls._realised_parent_classes.extend(u)
            return super().get_actualized_entity(cls, onto, **attrs)
        else:
            return super().get_actualized_entity(cls, onto, **attrs)

    def get_generated_inverse(self, cls: OwlObjectProperty, onto: Ontology) -> Type:
        cls.inverse_prop.inverse_prop = None
        return self.get_actualized_entity(cls.inverse_prop, onto)


class Owlready2Actualizer(OntologyActualizer):
    class_actualizer = OwlreadyClassActualizer()
    property_actualizer = OwlreadyPropertyActualizer()
