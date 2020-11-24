from typing import Any, Dict, List, Type, Union

from owlready2 import AnnotationProperty, DataProperty

from ..base import Ontology, OwlEntity, BUILTIN_DATA_TYPES, DATATYPE_MAP
from ..base.namespaces import RDFS_RANGE, OWL_INVERSE_OF
from ..wrapper import apply_classes_from
from ontogen.utils.classexp import ClassExpToConstruct

__all__ = ('OwlProperty', 'OwlAnnotationProperty',
           'OwlDataProperty', 'ENTITIES')

ENTITIES: Dict[str, OwlEntity] = {}


def get_exp_constructor(onto: Ontology):
    return ClassExpToConstruct(onto)


def get_equivalent_datatype(entity_name: str) -> Union[type, str]:
    return DATATYPE_MAP.get(entity_name, entity_name)


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

    def __init__(self, entity_qualifier: str):
        super(OwlProperty, self).__init__(entity_qualifier)
        self.range = []
        self.domain = []
        self.inverse_prop: Type or None = None

    # owlready-related implementation
    def actualize(self, onto: Ontology):
        """Instantiates a Property into a given Ontology

        Args:
            onto: An `owlready2` Ontology

        Returns:
            None
        """
        if self.name in ["topObjectProperty", "topDataProperty"]:
            return
        super().actualize(onto)
        apply_classes_from(onto)
        p = self._get_generated_class(onto, domain=self._get_generated(onto, self.domain),
                                      range=self._get_generated(onto, self.range))
        self.actualize_assertions(p)

    def _get_generated(self, onto: Ontology, classes: List[OwlEntity]):
        lst = []
        for c in classes:
            if isinstance(c, OwlEntity):
                c = c._get_generated_class(onto)
            lst.append(c)
        return lst

    def from_dict(self, sub: Dict[str, Any]):
        super(OwlProperty, self).from_dict(sub)
        self.range = sub.get(RDFS_RANGE, [])
        inv = sub.get(OWL_INVERSE_OF, [])
        if len(inv) == 1:
            self.inverse_prop = inv[0]


class OwlDataProperty(OwlProperty):
    name = "DataProperty"
    range = [str]
    _parent_class = DataProperty

    def from_dict(self, sub: Dict[str, Any]):
        super().from_dict(sub)
        self.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]


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



