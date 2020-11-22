from typing import Union


def assign_optional_dct(dct: dict, key: str, val: Union[dict, list]):
    if len(val) > 0:
        dct[key] = val


def absolutize_entity_name(name: str, fallback_prefix: str = "mao") -> str:
    return name if ":" in name else f"{fallback_prefix}:{name}"
