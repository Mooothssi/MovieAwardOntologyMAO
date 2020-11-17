from typing import Iterable, Union


def get_md_list(level: int, lst: Iterable[Union[str, Iterable[str]]]) -> str:
    """Returns a markdown list indented to the appropriate level.

    Args:
        level: The base level to indent to.
        lst: The list of (list of) str to convert to markdown.

    Examples:
        >>> get_md_list(5, [])
        ''
        >>> get_md_list(0, ['Thing'])
        '- Thing'
        >>> get_md_list(2, ['Pizza','Basil'])
        '    - Pizza\\n    - Basil'
        >>> get_md_list(0, ['Ant', ['Ant man', 'Ant woman']])
        '- Ant\\n  - Ant man\\n  - Ant woman'

    Notes:
        Base list item must be `str` in order to support
        multiple types of iterables. Either the list item
        type is defined or the iterable type is defined.
        I chose the former.
    """
    if isinstance(lst, str):
        return ''.join(('  ' * level, '- ', lst))
    if isinstance(lst, Iterable):
        return '\n'.join(get_md_list(level + 1, item) for item in lst)
    raise TypeError(f"item must be a str or an iterable of str, not {lst.__class__.__name__}")
