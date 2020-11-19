from typing import Any, Dict, List, Type

from owlready2 import AnnotationProperty, DataProperty

from ..base import Ontology, OwlEntity
from ..wrapper import apply_classes_from
from ..utils import ClassExpToConstruct

__all__ = ('OwlAnnotationProperty',
           'OwlDataProperty',
           'ENTITIES')

BUILTIN_DATA_TYPES = (str, int, float)
ENTITIES: Dict[str, OwlEntity] = {}


def get_exp_constructor(onto: Ontology):
    return ClassExpToConstruct(onto)


def check_restrictions(prefix: str, str_types: List[str], value: Any) -> bool:
    t = type(value)
    # check for builtin types
    if t in BUILTIN_DATA_TYPES:
        return True
    p = set([f"{prefix}:{str_type}" for str_type in str_types]).intersection(ENTITIES.keys())
    return len(p) > 0


class OwlProperty(OwlEntity):
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
        return [x._get_generated_class(onto) for x in self.range if isinstance(x, OwlEntity)]


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


