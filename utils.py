def select_not_null(dct: dict, *keys: str) -> dict:
    """Return a new dict with specified keys with values that are not null."""
    if keys:
        return {k: dct[k] for k in keys if dct.get(k) is not None}
    return {k: v for k, v in dct.items() if v is not None}
