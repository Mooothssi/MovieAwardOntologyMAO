import string

__all__ = ['snake_to_camel', 'camel_to_snake', 'to_constant']


def snake_to_camel(s: str) -> str:
    """Returns a new str in camelCase, given an str in snake_case.
    Removes all underscore before and after.

    Examples:
        >>> snake_to_camel('snake_to_camel')
        'snakeToCamel'
        >>> snake_to_camel('__snake_to_camel__')
        'snakeToCamel'
        >>> snake_to_camel('snakeToCamel')
        'snakeToCamel'
        >>> snake_to_camel('lonesnake')
        'lonesnake'
    """
    try:
        first, *others = [word for word in s.split('_') if word]
        return first + ''.join(s.title() for s in others)
    except ValueError:
        return s


def camel_to_snake(s: str) -> str:
    """Returns a new str in snake_case, given an str in camelCase.

    Raises:
        ValueError: When original str is not in camelCase

    Examples:
        >>> camel_to_snake('camelToSnake')
        'camel_to_snake'
        >>> camel_to_snake('camel_to_snake')
        Traceback (most recent call last):
          ...
        ValueError: original str is not in camelCase: 'camel_to_snake'
        >>> camel_to_snake('lonecamel')
        'lonecamel'
    """
    if '_' in s:
        raise ValueError('original str is not in camelCase: \'{}\''
                         .format(s))
    for u in string.ascii_uppercase:
        s = s.replace(u, '_' + u.lower())
    return s


def to_constant(s: str) -> str:
    """Returns a new str in CONSTANT_CASE, given any str.

    Examples:
        >>> to_constant('to_constant')
        'TO_CONSTANT'
        >>> to_constant('Meals, Entrees, and Side Dishes')
        'MEALS_ENTREES_AND_SIDE_DISHES'
        >>> to_constant('American Indian/Alaska Native Foods')
        'AMERICAN_INDIANALASKA_NATIVE_FOODS'
    """
    s = s.replace(' ', '_')
    s = ''.join(c.upper() for c in s if c in string.ascii_letters or c in '_')
    assert s.isidentifier(), s
    return s


def trim_spaces(s: str) -> str:
    """Trims excess spaces

    Examples:
        >>> trim_spaces(' pretty')
        'pretty'
        >>> trim_spaces(' CHEDDAR CHEESE')
        'CHEDDAR CHEESE'
        >>> trim_spaces(' salt  ')
        'salt'
    """
    return ' '.join(_ for _ in s.split(' ') if _)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
