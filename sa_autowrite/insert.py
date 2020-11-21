from importlib import import_module
from pathlib import Path
from typing import Union, List, Dict, IO, Type, Callable, Any

import pandas as pd

from dirs import ROOT_DIR
from engine import Session
from extended_csv import get_dialect_from_suffix
from sa_autowrite.hint import DeclaredModel
from sa_autowrite.model import TYPE_CONVERTER, DEF_TYPE
from sa_autowrite.create import _get_info_from_filename
from utils.str_utils import snake_to_capwords, snake_case
from sqlalchemy.sql.sqltypes import TypeEngine


# def read_in_chunks(file_object, chunk_size=1024):
#     """Lazy function (generator) to read a file piece by piece.
#     Default chunk size: 1k."""
#     while True:
#         data = file_object.read(chunk_size)
#         if not data:
#             break
#         yield data


def get_converter(col_type: TypeEngine) -> Callable[[str], Any]:
    if col_type.python_type == str:
        return str
    return TYPE_CONVERTER[col_type.python_type]


def create_instance(cls: Type[DeclaredModel], row: pd.Series,
                    *,
                    null_values: List[str] = None,
                    ignore_cols: List[str] = None,
                    ) -> DeclaredModel:
    if null_values is None:
        null_values = []
    if ignore_cols is None:
        ignore_cols = []

    data = {}

    for col in cls.__table__.columns:
        if col.name in ignore_cols:
            continue

        val = row.get(col.name)
        assert val is not None
        if val in null_values:
            val = None
        val = get_converter(col.type)(val)
        data[col.name] = val
    return cls(**data)


def insert_xsv_data(filename: Union[str, Path],
                    model_cls: Type[DeclaredModel],
                    *,
                    chunksize: int,
                    null_values: List[str],
                    ignore_cols: List[str],
                    encoding: str = None,
                    skip_rows_data: int = None,
                    read_lines_data: int = None,
                    verbose: int = 2
                    ):
    filename = Path(filename)

    if encoding is None:
        encoding = 'utf-8'
    if skip_rows_data is None:
        skip_rows_data = 1
    if skip_rows_data % chunksize != 0:
        raise ValueError(f"skip_rows_data must be a multiple of chunk_size")
    if read_lines_data % chunksize != 0:
        raise ValueError(f"read_lines_data must be a multiple of chunk_size")
    read_until = skip_rows_data + read_lines_data

    info = _get_info_from_filename(filename.name)
    dialect = get_dialect_from_suffix(info['format'])
    print(f"Opening {filename.name}")

    reader = pd.read_csv(filename, encoding=encoding, dialect=dialect, chunksize=chunksize)
    session = Session()
    counter = 0
    for chunk in reader:
        chunk: pd.DataFrame
        if counter < skip_rows_data:
            counter += chunksize
            continue
        for row in chunk.iterrows():
            line, series = row
            counter += 1
            session.add(create_instance(model_cls, series, null_values=null_values, ignore_cols=ignore_cols))
            if verbose > 1:
                if counter % 5000 == 0:
                    print(f"Added till row {counter}")
        session.commit()
        if verbose > 0:
            print(f'Committed till row {counter}')
        if counter == read_until:
            break


# Depreciated
def insert_data(in_directory: Union[str, Path],
                out_directory: Union[str, Path],
                *,
                null_values: List[str]) -> None:
    # Ensure directories are of type 'Path'
    in_directory = Path(in_directory)
    out_directory = Path(out_directory)

    module_names = []
    for pyfile in out_directory.glob('*.py'):
        if pyfile.name in ['base.py', '__init__.py']:
            continue
        module_names.append(pyfile.stem)
    class_names = [snake_to_capwords(name) for name in module_names]

    # invalidate_caches()
    path_to_package = Path(out_directory).relative_to(ROOT_DIR.absolute())
    package_path = str(path_to_package).replace('/', '.').replace('\\', '.')
    generated_package = import_module(package_path)
    models: Dict[str, DeclaredModel] = {class_name: generated_package.__dict__[class_name] for class_name in
                                        class_names}

    #
    session = Session()
    for csvfile in in_directory.glob('*.*sv'):
        info = _get_info_from_filename(csvfile.name)
        model_name = info['name']
        dialect = get_dialect_from_suffix(info['format'])
        print(f"Opening {csvfile}")

        class_name = snake_to_capwords(snake_case(model_name))
        if class_name not in class_names:
            raise AssertionError("class name from data files doesn't match models")
        print(f"Writing from {csvfile} to {class_name}\n")
        counter = 0
        for chunk in pd.read_csv(csvfile, chunksize=10_000, dialect=dialect):
            df = chunk
            instances = []
            for i in range(len(df)):
                model = models[class_name]
                datab = {}
                for col in model.__table__.columns:
                    try:
                        val = df.get(col.name)[counter]
                        type_ = repr(col.type)[:-2]
                        if type_ != 'String':
                            try:
                                val = TYPE_CONVERTER[DEF_TYPE[type_]](val)
                            except ValueError:
                                if val in null_values:
                                    val = None
                                else:
                                    raise
                        datab[col.name] = val
                    except TypeError:
                        if col.name == '_id':
                            pass
                        else:
                            raise
                instance = model(**datab)
                instances.append(instance)
                counter += 1
                if counter % 1000 == 0:
                    session.add_all(instances)
                    session.commit()
                    instances = []
                    print(f'Commited {counter}')
            if instances:
                session.add_all(instances)
                session.commit()
