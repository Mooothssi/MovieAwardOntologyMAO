__all__ = ['select_not_null', 'get_differing_keys_and_values']


def select_not_null(dct: dict, *keys: str) -> dict:
    """Return a new dict with specified keys with values that are not null."""
    if keys:
        return {k: dct[k] for k in keys if dct.get(k) is not None}
    return {k: v for k, v in dct.items() if v is not None}


def get_differing_keys_and_values(dct: dict) -> dict:
    return {k: v for k, v in dct.items() if k != v}
