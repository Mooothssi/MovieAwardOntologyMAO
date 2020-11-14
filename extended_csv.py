import csv
from itertools import islice

from typing import List, Dict, Iterable, TextIO

from utils import select_not_null


def get_differing_keys_and_values(dct: dict) -> dict:
    return {k: v for k, v in dct.items() if k != v}


def read_xsv_file(filename: str,
                  dialect: str,
                  *,
                  encoding: str = None,
                  fieldnames: List[str] = None,
                  first_line_is_column_header: bool = True,
                  discard: int = None,
                  load_at_most: int = None,
                  ) -> List[Dict]:
    """Returns a list of dicts. Convenience method for `read_xsv`.

    Args:
        filename:
            The filename to open.
        dialect:
            As used in built-in module `csv`.
        encoding:
            Encoding of the file to open.
        fieldnames:
            TODO: Pending documentation for 'fieldnames'
        first_line_is_column_header:
            If True, parses first line as column headers.
        discard:
            Non-negative integer or None. Initial rows of _data_ to discard.
        load_at_most:
            Non-negative integer or None. Rows of _data_ to load.

    Notes:
        Use 'excel' dialect for CSV. Use 'excel-tab' for TSV.
    """
    kwargs = {
        'encoding': encoding,
        'fieldnames': fieldnames,
        'first_line_is_column_header': first_line_is_column_header,
        'discard': discard,
        'load_at_most': load_at_most,
    }
    with open(filename, 'r', **select_not_null(kwargs, 'encoding')) as file:
        kwargs.pop('encoding')
        # must iterated now because file will be closed
        return list(read_xsv(file, dialect, **select_not_null(kwargs)))


def read_xsv(file: TextIO,
             dialect: str,
             fieldnames: List[str] = None,
             first_line_is_column_header: bool = True,
             discard: int = None,
             load_at_most: int = None,
             ) -> Iterable[Dict]:
    """Returns an iterable of dict. Must be iterated while file is still open.

    Args:
        file:
            An open file.
        dialect:
            As used in built-in module `csv`.
        fieldnames:
            TODO: Pending documentation for 'fieldnames'
        first_line_is_column_header:
            If True, parses first line as column headers.
        discard:
            Non-negative integer or None. Initial rows of _data_ to discard.
        load_at_most:
            Non-negative integer or None. Rows of _data_ to load.

    Notes:
        Use 'excel' dialect for CSV. Use 'excel-tab' for TSV.

    Warnings:
        Must be iterated while file is still open.
    """
    kwargs = {
        'fieldnames': fieldnames,
    }

    if not first_line_is_column_header and fieldnames is None:
        # use 'Column X' as fieldnames like in OpenRefine
        first_line = file.readline(1)
        file.seek(-1)
        delimiter = csv.get_dialect(dialect).delimiter
        num_cols = len(first_line.split(delimiter))
        kwargs['fieldnames'] = [f'Column {i + 1}' for i in range(num_cols)]

    reader = csv.DictReader(file, **select_not_null(kwargs, 'fieldnames'))

    if first_line_is_column_header and fieldnames is not None:
        raise NotImplementedError("Changing column names isn't supported for simplicity")

    stop = None
    if load_at_most is not None:
        stop = load_at_most
        if discard is not None:
            stop += discard

    return islice(reader, discard, stop)
