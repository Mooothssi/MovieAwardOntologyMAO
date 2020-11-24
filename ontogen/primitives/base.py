from typing import Any, Dict, List, Type

from owlready2 import AnnotationProperty, DataProperty

from ..base import Ontology, OwlEntity, BUILTIN_DATA_TYPES
from ..wrapper import apply_classes_from
from ontogen.utils.classexp import ClassExpToConstruct

__all__ = ('OwlProperty', 'OwlAnnotationProperty',
           'OwlDataProperty', 'ENTITIES')

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
        super().actualize(onto)
        apply_classes_from(onto)
        p = self._get_generated_class(onto, range=self.get_generated_range(onto))
        self.actualize_assertions(p)

    def get_generated_range(self, onto: Ontology):
        lst = []
        for x in self.range:
            if isinstance(x, OwlEntity):
                x = x._get_generated_class(onto)
            lst.append(x)
        return lst


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



