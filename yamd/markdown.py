from typing import Sequence, Union


def get_md_list(level: int, lst: Sequence[Union[str, Sequence[str]]]) -> str:
    """Returns a markdown list indented to the appropriate level.

    Args:
        level: The base level to indent to.
        lst: The list of (list of) str to convert to markdown.

    Examples:
        >>> get_md_list(5, [])
        ''
        >>> get_md_list(-1, ['Thing'])
        '- Thing'
        >>> get_md_list(1, ['Pizza','Basil'])
        '    - Pizza\\n    - Basil'
        >>> get_md_list(0, ['Ant', ['Ant man', 'Ant woman']])
        '  - Ant\\n    - Ant man\\n    - Ant woman'
        >>> get_md_list(0, [{'@type': 'Person', 'name': 'Charlie'}, {}])
        Traceback (most recent call last):
          ...
        TypeError: item must be a str or an iterable of str, not 'dict'

    Notes:
        Base list item must be `str` in order to support
        multiple types of iterables. Either the list item
        type is defined or the iterable type is defined.
        I chose the former.
    """
    if isinstance(lst, str):
        return ''.join(('  ' * level, '- ', lst))
    if isinstance(lst, (Sequence, map)):
        return '\n'.join(get_md_list(level + 1, item) for item in lst)
    raise TypeError(f"item must be a str or an iterable of str, not '{lst.__class__.__name__}'")


if __name__ == '__main__':
    import doctest

    doctest.testmod()
