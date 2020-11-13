import datetime


def _parse_date_by_guessing(date_str: str, sep: str = None) -> datetime.date:
    """Strategy for unknown date formats.

    Args:
        date_str (str): The date which may not be in standard ISO format

    Raises:
        ValueError: When the function cannot parse the date given
    """
    try:
        return datetime.date.fromisoformat(date_str)
    except ValueError:
        pass
    for sep_ in (sep, '-', '/', ':', ' '):
        parts = date_str.split(sep=sep_)
        if len(parts) != 3:
            continue
        for i in range(len(parts)):
            if len(parts[i]) == 4:
                break
        else:
            raise ValueError('Cannot parse \'{}\', cannot determine year'.format(date_str))
        if i == 2:
            # MM/DD/YYYY or DD-MM-YYYY
            try:
                assert 0 < int(parts[0]) <= 12
                assert 0 < int(parts[1]) <= 31
                if sep_ == '/':
                    import warnings
                    warnings.warn('Assuming MM/DD/YYYY format')
                    # Only Americans use the slashes and not the ISO standard
                    return datetime.date(int(parts[2]), int(parts[0]), int(parts[1]))
                assert sep_ != '/'
                raise ValueError('the parser is not sure what to do') from Exception
            except AssertionError:
                try:
                    assert 0 < int(parts[0]) <= 31
                    assert 0 < int(parts[1]) <= 12
                    return datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
                except AssertionError:
                    raise ValueError('the parser is not sure what to do') from Exception
        elif i == 0:
            # YYYY-MM-DD
            return datetime.date(*map(int, parts))
        raise ValueError('the parser is not sure what to do')
    raise ValueError('the parser is not sure what to do')


def _parse_date_with_format(date_str: str, sep: str, format: str) -> datetime.date:
    """Strategy for known date formats.

    Args:
        date_str (str): The date which may not be in standard ISO format
        sep: The separator used to separate each time unit
        format: Format of `date_str`, 'DMY' 'YMD' or 'MDY'

    Raises:
        ValueError: When the value doesn't make sense
    """
    parts = date_str.split(sep)
    if len(parts) != 3:
        raise ValueError('parts is not 3: {}'.format(parts))
    if format == 'DMY':
        return datetime.date.fromisoformat(
            '{}-{:0>2}-{:0>2}'.format(parts[2], parts[1], parts[0]))
    if format == 'YMD':
        return datetime.date.fromisoformat(
            '{}-{:0>2}-{:0>2}'.format(parts[0], parts[1], parts[2]))
    if format == 'MDY':
        return datetime.date.fromisoformat(
            '{}-{:0>2}-{:0>2}'.format(parts[2], parts[0], parts[1]))


def parse_date(date_str: str, sep: str = None, format: str = None) -> datetime.date:
    """Returns a ``datetime.date`` if possible

    Args:
        date_str (str): The date which may not be in standard ISO format
        sep: Optional. The separator used to separate each time unit
        format: Optional. Format of `date_str`, 'DMY' 'YMD' or 'MDY'

    Raises:
        ValueError: When the function cannot parse the date given

    Examples:
        >>> parse_date('55 13 2019')
        Traceback (most recent call last):
          ...
        ValueError: the parser is not sure what to do
        >>> parse_date('4/1/2019')  # check if there is warning
        datetime.date(2019, 4, 1)
        >>> parse_date('4-1-2019')
        Traceback (most recent call last):
          ...
        ValueError: the parser is not sure what to do
        >>> parse_date('4-1-2019', sep='-', format='DMY')
        datetime.date(2019, 1, 4)
        >>> parse_date('14-1-2019')
        datetime.date(2019, 1, 14)
    """
    if sep is not None:
        if format is not None:
            return _parse_date_with_format(date_str, sep, format)
        return _parse_date_by_guessing(date_str, sep)
    if format is not None:
        raise NotImplementedError
    return _parse_date_by_guessing(date_str)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
