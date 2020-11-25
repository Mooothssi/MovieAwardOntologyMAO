from typing import Any, Dict, List, Type, Union

from ontogen.base import OwlEntity, BUILTIN_DATA_TYPES, DATATYPE_MAP

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
