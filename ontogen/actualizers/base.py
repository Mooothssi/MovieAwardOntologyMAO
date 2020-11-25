from abc import ABCMeta, abstractmethod
from typing import Type

from ontogen.primitives.base import OwlEntity
from ontogen.base.ontology import Ontology
from ontogen.primitives.classes import OwlClass
from ontogen.primitives.properties import OwlProperty


class OntologyBaseActualizer(metaclass=ABCMeta):
    def __init__(self, parent: 'OntologyActualizer'):
        self.parent = parent

    def actualize(self, cls: OwlEntity, onto: Ontology):
        """Makes the entity concrete (saved) in a given Ontology

        Args:
            cls: A given Entity
            onto: A given Ontology

        Returns:
            None
        """
        if cls._use_default_prefix:
            cls.prefix = onto.base_prefix

    @abstractmethod
    def get_actualized_entity(self, cls: OwlEntity, onto: Ontology, **attrs: dict) -> object:
        """Returns the entity concrete (saved) in a given Ontology

        Args
            cls: A given Entity
            onto: A given Ontology
            **attrs: A dict of keyword arguments required to instantiate underlying implementation

        Returns:
            An actualized OwlEntity
        """
        raise NotImplementedError


class OntologyActualizer:
    class_actualizer_class: Type[OntologyBaseActualizer] = None
    property_actualizer_class: Type[OntologyBaseActualizer] = None

    def __init__(self, onto: Ontology):
        self.onto = onto
        self.class_actualizer = self.class_actualizer_class(self)
        self.property_actualizer = self.property_actualizer_class(self)

    def actualize(self, entities: dict):
        for key, item in entities.items():
            if isinstance(item, OwlClass):
                self.class_actualizer.actualize(cls=item, onto=self.onto)
            elif isinstance(item, OwlProperty):
                self.property_actualizer.actualize(cls=item, onto=self.onto)
        for indiv in self.onto.individuals.values():
            indiv.actualize_assertions(indiv._imp)
