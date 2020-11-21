import re
from pathlib import Path
from typing import IO, Any, Dict, List, Union

import pandas as pd

from extended_csv import get_dialect_from_suffix, read_xsv_file
from sa_autowrite.model import Table
from utils.dict_utils import select_not_null
from utils.io_utils import open_and_write_file
from utils.str_utils import snake_to_capwords, snake_case

__all__ = ['write_models', 'write_model', 'write_base']


def write_model(file: Union[IO, str, Path],
                model_name: str,
                data: List[Dict[str, Any]],
                *,
                gen_pk: bool = True,
                pk_cols: List[str] = None):
    kwargs = {
        'pk_cols': pk_cols,
        'gen_pk': gen_pk
    }

    df = pd.DataFrame(data)
    table = Table(model_name, df, **select_not_null(kwargs))
    open_and_write_file(file, table.as_python())


def write_base(file: Union[IO, str, Path]) -> None:
    """Writes the file that defines SQL Alchemy declarative base.

    Args:
        file: An open file (IO) or filename (str/Path) to write the SQL Alchemy
            declarative base which will be imported in models to.

    Returns:
        None
    """
    lines = [
        'from sqlalchemy.ext.declarative import declarative_base',
        '',
        'Base = declarative_base()',
        '',
    ]
    open_and_write_file(file, '\n'.join(lines))


def _get_info_from_filename(filename: str) -> dict:
    """Returns model name and other infos given filename in some naming convention.

    Examples:
        >>> _get_info_from_filename('branded_food-1000.csv')
        {'name': 'branded_food', 'num_rows': 1000, 'format': 'csv'}
        >>> _get_info_from_filename('nutrients.csv')
        {'name': 'nutrients', 'num_rows': None, 'format': 'csv'}
        >>> _get_info_from_filename('BadNaming.tsv')
        {'name': 'BadNaming', 'num_rows': None, 'format': 'tsv'}
    """
    *parts, suffix = filename.split('.')
    dct = re.match(r'^(?P<name>[A-z0-9.]*)(-(?P<num_rows>[0-9]+))?$', '.'.join(parts)).groupdict()
    return {
        'name': dct['name'],
        'num_rows': int(dct['num_rows']) if dct['num_rows'] else None,
        'format': suffix,
    }


def write_models(in_directory: Union[str, Path],
                 out_directory: Union[str, Path],
                 *,
                 max_lines: int = None
                 ) -> None:
    """Writes models in `out_directory` from all CSV/TSV data in the `in_directory` to models.

    Assumes some naming convention of data files.

    Args:
        in_directory: Data directory to read from.
        out_directory: Models directory to write to.
        max_lines: Maximum number of lines of data to read.

    Returns:
        None
    """
    # Ensure directories are of type 'Path'
    in_directory = Path(in_directory)
    out_directory = Path(out_directory)

    module_class = []

    # Write models file
    for csvfile in in_directory.glob('*.*sv'):
        info = _get_info_from_filename(csvfile.name)
        model_name = info['name']
        dialect = get_dialect_from_suffix(info['format'])
        print(f"Reading from {csvfile}")
        module_name = snake_case(model_name)
        class_name = snake_to_capwords(module_name)
        module_class.append((module_name, class_name))
        write_model(out_directory / f'{module_name}.py',
                    class_name,
                    read_xsv_file(csvfile, encoding='utf-8', dialect=dialect, load_at_most=max_lines))
        print(f"Writing to {(out_directory / f'{snake_case(model_name)}.py')}\n")

    # Check for required files
    has_base = False
    for pyfile in out_directory.glob('*.py'):
        if pyfile.name == 'base.py':
            has_base = True

    # Write required files
    if not has_base:
        print(f'base.py not detected in {out_directory}, writing one')
        write_base((out_directory / 'base.py'))

    print(f'__init__.py generated.')
    lines = ['# import modules to run it through declarative base'] + \
            [f'from .{module_name} import {class_name}' for module_name, class_name in module_class] + \
            ['']
    open_and_write_file((out_directory / '__init__.py'), '\n'.join(lines))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
