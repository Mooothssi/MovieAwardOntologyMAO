import re
from pathlib import Path
from typing import IO, Any, Dict, List, Union

from pandas import DataFrame
from stringcase import pascalcase, snakecase

from extended_csv import get_dialect_from_suffix, read_xsv_file
from sa_autowrite.model import Table
from utils.io_utils import open_and_write_file
from utils.dict_utils import select_not_null


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

    df = DataFrame(data)
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
        {'nutrients': 'branded_food', 'num_rows': None, 'format': 'csv'}
        >>> _get_info_from_filename('BadNaming.tsv')
        {'BadNaming': 'branded_food', 'num_rows': None, 'format': 'tsv'}
    """
    dct = re.match(r'(?P<name>[A-z0-9]*)(-(?P<num_rows>[0-9]+))?(?P<format>.[a-z]+)?', filename).groupdict()
    return {
        'name': dct['name'],
        'num_rows': dct['num_rows'] if dct['num_rows'] else None,
        'format': dct['format'],
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
        with open(csvfile, 'r', encoding='utf-8') as f:
            print(f"Reading from {csvfile}")
            module_name = snakecase(model_name)
            class_name = pascalcase(model_name)
            module_class.append((model_name, class_name))
            write_model(out_directory / f'{module_name}.py',
                        class_name,
                        read_xsv_file(csvfile, dialect=dialect, load_at_most=max_lines))
            print(f"Writing to {(out_directory / f'{snakecase(model_name)}.py')}\n")

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


'''
Sample script (put this in the root dir:

from sa_autowrite.main import write_models

write_models('tests/data/csv/', 'sa_autowrite/out/', max_lines=1000)

'''


if __name__ == '__main__':
    import doctest
    doctest.testmod()
