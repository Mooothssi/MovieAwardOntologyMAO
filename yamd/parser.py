from typing import List


def parse_lenient_list_of_strings(obj) -> List[str]:
    if isinstance(obj, str):
        if obj:
            # assume using not using list for one string
            return [obj]
        # empty string, assume using '' as placeholder
        assert obj == ''
        return []
    if isinstance(obj, list):
        if all(isinstance(item, str) for item in obj):
            return obj
    raise ValueError(f"Object is not a list of strings: '{obj}'")


def is_recursive_list_of_strings(obj) -> bool:
    if isinstance(obj, str):
        return True
    if isinstance(obj, list):
        return all(is_recursive_list_of_strings(item) for item in obj)
    return False


def parse_lenient_list_of_list_of_string(obj) -> List[str]:
    if isinstance(obj, str):
        if obj:
            # assume using not using list for one string
            return [obj]
        # empty string, assume using '' as placeholder
        assert obj == ''
        return []
    if isinstance(obj, list):
        if is_recursive_list_of_strings(obj):
            return obj
    raise ValueError(f"Object is not a list of (list of) strings: '{obj}'")


def parse_lenient_list_of_objects(obj) -> List[dict]:
    if isinstance(obj, str):
        if obj == '':
            # empty string, assume using '' as placeholder
            return []
    if isinstance(obj, dict):
        # assume using not using list for one object
        return [obj]
    if isinstance(obj, list):
        if all(isinstance(item, dict) for item in obj):
            return obj
    raise ValueError(f"Object is not a list of dicts: '{obj}'")
