from abc import abstractmethod
from typing import IO, Iterable, Sequence, overload, TypeVar
from utils.dict_utils import select_not_null
import pandas as pd

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


def parse_imdb_list(file: IO, chunksize: int) -> pd.DataFrame:

    return pd.DataFrame

MAP = {
    'csv': parse_csv,
    'tsv': parse_tsv,
    'list': parse_imdb_list,
}
