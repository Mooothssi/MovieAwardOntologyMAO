from abc import abstractmethod
from pathlib import Path
from typing import IO, Iterable, Sequence, overload, TypeVar, Union, Iterator, Tuple
from utils.dict_utils import select_not_null
import pandas as pd
import re

__all__ = ['MAP']


def parse_csv(file: IO, chunksize: int = None) -> pd.DataFrame:
    kwd = {
        chunksize: chunksize
    }
    return pd.read_csv(file, dialect='excel', **select_not_null(kwd))


def parse_tsv(file: IO, chunksize: int = None) -> pd.DataFrame:
    kwd = {
        chunksize: chunksize
    }
    return pd.read_csv(file, dialect='excel-tab', **select_not_null(kwd))


def get_data_lines(filename: Union[str, Path], encoding: str = 'utf-8') -> str:
    with open(filename, 'r', encoding=encoding) as file:
        line = ''
        while not line.startswith('---'):
            line = file.readline()
        # maybe do sth or maybe not
        while not line.startswith('==='):
            line = file.readline()
        # now at data
        while not line.startswith('---'):
            line = file.readline()
            yield line
    raise StopIteration


def consume_str_until(it: Iterator[str], stop: str) -> None:
    """Reads an iterator of str until 'stop'.

    Args:
        it: The iterator of the string to read
        stop: The character to stop

    Returns:
        None

    Notes:
        Consumes the stop character in the iterator.

    Warnings:
        'stop' must be a character but isn't checked to increase performance(?).
    """
    while next(it) != stop:
        pass
    return


def read_str_until(it: Iterator[str], stop: str) -> str:
    """Returns the string before stop.

    Args:
        it: The iterator of the string to read
        stop: The character to stop

    Notes:
        Consumes the stop character in the iterator.

    Warnings:
        'stop' must be a character but isn't checked to increase performance(?).
    """
    lst = []
    c = next(it)
    while c != stop:
        lst.append(c)
        c = next(it)
    return ''.join(lst)


def read_str_untils(it: Iterator[str], *stops: str) -> (str, str):
    """Returns the string before stop.

    Args:
        it: The iterator of the string to read
        *stop: The characters to stop

    Notes:
        Consumes the stop character in the iterator.

    Warnings:
        'stop' must be a character but isn't checked to increase performance(?).

    Returns:
        result, stopped character
    """
    lst = []
    c = next(it)
    while c not in stops:
        lst.append(c)
        c = next(it)
    return ''.join(lst), c


def parse_line_iter(line: str) -> Tuple[str, str, str, str, bool, str]:
    """Parse a line in IMDB list file using iterator method.

    Args:
        line: The line to parse

    Returns:
        title, year, episode, episode_num, and rest.
        episode and episode_num will be None if it doesn't exist.

    Examples:
        # >>> parse_line_iter('"!Next?" (1994)\\t\\t\\t\\t\\t\\tItaly\\n')  # countries.list
        # ('!Next?', '1994', None, None, 'Italy')
        # >>> parse_line_iter('"#1 Single" (2006)\\t\\t\\t\\t\\tUSA\\n')
        # ('#1 Single', '2006', None, None, 'USA')
        # >>> parse_line_iter('"#15SecondScare" (2015)\\t\\t\\t\\t\\tUSA\\n')
        # ('#15SecondScare', '2015', None, None, 'USA')
        # >>> parse_line_iter('"#15SecondScare" (2015) {Because We Don\\'t Want You to Fall Asleep (#1.3)}\\tUSA\\n')
        # ('#15SecondScare', '2015', "Because We Don't Want You to Fall Asleep", '1.3', 'USA')
        # >>> parse_line_iter('"#1 Single" (2006) {Wingman (#1.6)}\\t\\t\\tStick Figure Productions [us]\\n')  #production-companies.list
        # ('#1 Single', '2006', 'Wingman', '1.6', 'Stick Figure Productions [us]')
        # >>> parse_line_iter('"#1MinuteNightmare" (2014)\\t\\t\\t\\tSuperfreakMedia [gb]\\n')  #production-companies.list
        # ('#1MinuteNightmare', '2014', None, None, 'SuperfreakMedia [gb]')
        # >>> parse_line_iter('"#7DaysLater" (2013)\\t\\t\\t\\t\\tLudo Studio [au]\\n')  #production-companies.list
        # ('#7DaysLater', '2013', None, None, 'Ludo Studio [au]')
        # >>> parse_line_iter('"#LoveMonkeyChocolateFlowers" (2014)\\t\\t\\tUK:PG\\n')  #certificates.list
        # ('#LoveMonkeyChocolateFlowers', '2014', None, None, 'UK:PG')
        # >>> parse_line_iter('"$#*! My Dad Says" (2010)\\t\\t\\t\\tAustralia:PG\\n')  #certificates.list
        # ('$#*! My Dad Says', '2010', None, None, 'Australia:PG')
        # >>> parse_line_iter('"$#*! My Dad Says" (2010) {Code Ed (#1.4)}\\t\\tNetherlands:6\\n')  #certificates.list
        # ('$#*! My Dad Says', '2010', 'Code Ed', '1.4', 'Netherlands:6')
        # >>> parse_line_iter('"1714. El preu de la llibertat" (2014) {{SUSPENDED}}\\tSpain\\n')  #countries.list
        # ('1714. El preu de la llibertat', '2014', None, None, None, 'Spain')
        # >>> parse_line_iter('"18 Wheels of Justice" (2000) {(2000-03-29)}\\t\\tUSA\\n')  #countries.list
        # ('$#*! My Dad Says', '2010', 'Code Ed', '1.4', 'Netherlands:6')
    """
    it = iter(line)
    if next(it) != '"':
        raise AssertionError(f"line '{line}' has incorrect format (expecting '\"' at position 0)")
    title = read_str_until(it, '"')
    consume_str_until(it, '(')
    year = read_str_until(it, ')')
    c = next(it)
    if c == ' ':
        if next(it) != '{':
            raise AssertionError(f"line '{line}' has incorrect format (expecting '{{')")
        try:
            episode, stop = read_str_untils(it, '(', '}')
        except StopIteration as e:
            raise AssertionError(f"line '{line}' has incorrect format (expecting '(')") from e
        episode = episode.rstrip(' ')
        if stop == '(':
            if episode:
                if next(it) != '#':
                    raise AssertionError(f"line '{line}' has incorrect format (expecting '#')")
                episode_num = read_str_until(it, ')')
                if next(it) != '}':
                    raise AssertionError(f"line '{line}' has incorrect format (expecting '}}')")
            else:
                episode = ''.join(['(', read_str_until(it, ')'), ')'])
                if next(it) != '}':
                    raise AssertionError(f"line '{line}' has incorrect format (expecting '}}')")
                episode_num = None
        else:
            episode_num = None
    else:
        episode = None
        episode_num = None
    c = next(it)
    while c == '\t':
        c = next(it)
    rest = c + read_str_until(it, '\n')
    is_suspended = False
    return title, year, episode, episode_num, is_suspended, rest


def parse_line_re(line: str) -> dict:
    """Parse a line in IMDB list file using regex method.

    Args:
        line: The line to parse

    Returns:
        title, year, episode, episode_num, and rest.
        episode and episode_num will be None if it doesn't exist.

    Examples:
        See unittest.

    Raises:
        ValueError when line does not match regex
    """
    m = re.match(r'(?P<title>.*) \((?P<year>(\d\d\d\d)|(\?\?\?\?))(/(?P<roman>[IVXLCDM]+))?\)( \((?P<type>\S*)\))?( {(?P<episode_info>.*)?})?\t+(?P<data>.*)\n?', line)
    try:
        dct = m.groupdict()
    except AttributeError as e:
        raise ValueError(f"line doesn't match regex: {line}") from e
    title = dct.get('title')
    year = dct.get('year')
    out = {
        'title': title[1:-1] if title[0] == title[-1] == '"' else title,
        'year': None if year == '????' else int(year),
        'roman': dct.get('roman'),
        'type': dct.get('type'),
        'episode_info': dct.get('episode_info'),
        'data': dct.get('data'),
    }
    return out


def parse_imdb_list(filename: Union[str, Path], *, chunksize: int, encoding: str = None) -> pd.DataFrame:
    count = 0
    lst = []
    for line in get_data_lines(filename, encoding=encoding):
        try:
            dct = parse_line_re(line)
        except ValueError:
            if line.startswith('---'):
                # last line
                return
            else:
                raise
        else:
            lst.append(dct)
            count += 1
            if count % chunksize == 0:
                yield pd.DataFrame(lst)
                lst = []

MAP = {
    'csv': parse_csv,
    'tsv': parse_tsv,
    'list': parse_imdb_list,
}
