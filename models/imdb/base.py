def clean_backslash_n(obj: any, prop_name: str):
    if hasattr(obj, prop_name):
        if getattr(obj, prop_name) == r'\N':
            setattr(obj, prop_name, None)


def clean_backslash_n_multiple(obj: any, prop_list: list[str]):
    for prop in prop_list:
        clean_backslash_n(obj, prop)
