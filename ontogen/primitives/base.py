from typing import Any, Dict, List, Type, Union

from ontogen.base import OwlEntity, BUILTIN_DATA_TYPES, DATATYPE_MAP
from ontogen.base.namespaces import RDFS_RANGE, OWL_INVERSE_OF, RDFS_DOMAIN

__all__ = ('OwlProperty', 'OwlAnnotationProperty',
           'OwlDataProperty', 'ENTITIES')

ENTITIES: Dict[str, OwlEntity] = {}


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

    def from_dict(self, sub: Dict[str, Any]):
        super(OwlProperty, self).from_dict(sub)
        self.range = sub.get(RDFS_RANGE, [])
        self.domain = sub.get(RDFS_DOMAIN, [])
        inv = sub.get(OWL_INVERSE_OF, [])
        if len(inv) == 1:
            self.inverse_prop = inv[0]


class OwlDataProperty(OwlProperty):
    name = "DataProperty"
    range = [str]

    def from_dict(self, sub: Dict[str, Any]):
        super().from_dict(sub)
        self.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]


class OwlAnnotationProperty(OwlProperty):
    name = "AnnotationProperty"
    range = [str]




