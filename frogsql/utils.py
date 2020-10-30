from typing import List, Dict, TypeVar, Iterable, Tuple, Any, Sequence, TextIO, Generator, Callable
import csv
from itertools import tee, zip_longest, islice

T = TypeVar('T')


def read_csv_file(filename: str, encoding: str = 'utf-8', default: Any = None, **kwargs) -> List[Dict]:
    """ Reads a csv file and return a list of dictionaries. """
    data = []
    if kwargs is not None:
        with open(filename, 'r', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    if key in kwargs:
                        try:
                            row[key] = kwargs[key](row[key])
                        except ValueError:
                            row[key] = default
                data.append(row)
    else:
        with open(filename, 'r', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    return data


def write_csv_file(filename: str, data: List[Dict], *, encoding: str = 'utf-8'):
    """ Write a list of dictionaries to csv file. """
    with open(filename, 'w', encoding=encoding, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, data[0].keys())
        writer.writeheader()
        for d in data:
            writer.writerow(d)


def trim_file(file: str):
    with open(file, 'r') as f:
        lines = f.read().splitlines()

    trimmed = []
    for line in lines:
        if line == '':
            continue
        trimmed.append(line)

    with open(file, 'w') as f:
        f.write('\n'.join(trimmed))


def knots_to_kmh(x: float) -> float:
    return x * 1.852


def km_to_mile(x: float) -> float:
    return x * 0.621371192


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...

    Taken from https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def capwords_to_snake_case(s: str) -> str:
    """

    >>> capwords_to_snake_case('BaseModel')
    'base_model'
    >>> capwords_to_snake_case('BillOfLading')
    'bill_of_lading'
    >>> capwords_to_snake_case('Port')
    'port'
    """
    chars = []
    for c in s:
        if c.isupper():
            chars.append('_')
            chars.append(c.lower())
        else:
            chars.append(c)
    return ''.join(islice(chars, 1, None))


if __name__ == '__main__':
    import doctest
    doctest.testmod()


def common_name_to_snake_case(s: str):
    """ 'Bill-Of-Lading Key' -> 'bill_of_lading_key' """
    chars = []
    for c in s:
        if c.isalnum():
            chars.append(c)
        else:
            if c in (' ', '-', '_'):
                chars.append(' ')
    # TODO: deal with numbers in front
    return ''.join(chars).replace(' ', '_').replace('-', '_').lower()
