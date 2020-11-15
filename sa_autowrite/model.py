from datetime import date, datetime
from typing import List

from pandas import DataFrame, Series

from utils.date_utils import parse_date
from utils.str_utils import camel_to_snake


def str_is_date(s: str) -> bool:
    """Check whether or not a string is a date"""
    try:
        parse_date(s)
        date.fromisoformat(s)
    except ValueError:
        return False
    else:
        return True


def str_is_datetime(s: str) -> bool:
    """Check whether or not a string is a datetime"""
    try:
        date.fromisoformat(s)
    except ValueError:
        return False
    else:
        return True


def str_is_integer(s: str) -> bool:
    """Check whether or not a string is lossless-ly an integer"""
    return s.isnumeric() and not s.startswith('0')


def str_is_float(s: str) -> bool:
    """Check whether or not a string is lossless-ly a float"""
    return s.isdecimal() and not s.startswith('0')


TYPE_CHECKER = {
    int: str_is_integer,
    float: str_is_float,
}
TYPE_CONVERTER = {
    date: parse_date,
    datetime: datetime.fromisoformat,
}
TYPE_DEF = {
    str: 'String',
    int: 'Integer',
    date: 'Date',
    datetime: 'DateTime',
    # TODO: Choose a SA representation of float
    float: 'Float',
}


class Table:
    """ Represents a database table/model. """
    def __init__(self,
                 name: str,
                 data: DataFrame,
                 *,
                 gen_pk: bool = True,
                 pk_cols: List[str] = None):
        """Creates an object storing model information.

        Args:
            name:
                The name of the model.
            data:
                The data to use to generate .py model.
            gen_pk:
                If True use a new column for the primary key.
                If False, must specify `pk_cols` to use.
            pk_cols:
                Columns to use as primary keys.
                Must match columns in the data.

        Raises:
            ValueError:
                When `gen_pk` is False and no `pk_cols` is specified.
                When a pk in`pk_cols` isn't found in the data.
        """
        self.name = name  # Name of the table in CapWords
        self.data = data
        self.columns = []
        self.pk_cols = pk_cols
        for name in data.columns:
            col = Column(name)
            for type, check in TYPE_CHECKER.items():
                if all(data.get(col.name).map(check)):
                    col.type = type
                    col.data = data.get(col.name).map(type)
                    break
            else:
                for type, convert in TYPE_CONVERTER.items():
                    try:
                        col.data = data.get(col.name).map(convert)
                        col.type = type
                        break
                    except ValueError:
                        pass
                else:
                    col.type = str
                    col.data = data.get(col.name)
            self.columns.append(col)

        if self.pk_cols is None:
            if gen_pk:
                self.columns.insert(0, Column('_id', Series(range(len(self.data))), type_=int, is_pk=True))
            else:
                raise ValueError(f"Table '{self.name}' will have no primary key if not specified")
        elif self.pk_cols:
            # pk_cols is not []
            for pk in self.pk_cols:
                for col in self.columns:
                    if col.name == pk:
                        col.is_pk = True
                        break
                else:
                    raise ValueError(f"Specified pk: '{pk}' does not match any columns in table '{self.name}'.\ncols = {self.columns}")

    def as_python(self) -> str:
        """ Returns the object as python code. """
        lines = [
            f"from sqlalchemy import Column, {', '.join(sorted(set(TYPE_DEF[col.type] for col in self.columns)))}",
            '',
            f'from .base import Base',
            '',
            '',
            f'class {self.name}(Base):',
            f"    __tablename__ = '{camel_to_snake(self.name)}'",
            '',
            *[col.as_python(2 + max(col.definition_len for col in self.columns)) for col in self.columns],
            '',
            '    def __repr__(self):',
            f'''        return f"<{self.name}({', '.join(f"{col.name}='{{self.{col.name}}}'" for col in self.columns)})>"''',
            ''
        ]
        return '\n'.join(lines)


class Column:
    """ Object to store column data to use in `Table`. """
    def __init__(self, name: str, data: Series = None, *, type_: type = None, is_pk: bool = False):
        self.name = name
        self.data: Series = data
        self.type: type = type_
        self.is_pk = is_pk
        self.comments: List[str] = []

    def __str__(self):
        """ Returns some data to id the object for debugging. """
        return f"Column(name={self.name}, type={self.type}, is_pk={self.is_pk})"

    def as_python(self, start: int = 55):
        """ Returns the object as python code. """
        return (f"    {{:<{start}}}").format(self.definition) + self.comment

    @property
    def definition(self) -> str:
        return f"{self.name} = Column({TYPE_DEF[self.type]}{', primary_key=True' if self.is_pk else ''})"

    @property
    def definition_len(self) -> int:
        return len(self.definition)

    @property
    def comment(self) -> str:
        self.comments.append(f'unique: {len(self.data.unique())}')
        if self.type in [int, float, date]:
            self.comments.append(f'val = [{self.data.min()},{self.data.max()}]')
        elif self.type == str:
            lens = self.data.map(len)
            un = sorted(lens.unique())
            if len(un) < 10:
                self.comments.append(f"len = {{{','.join(map(str, un))}}}")
            else:
                self.comments.append(f'len = [{lens.min()},{lens.max()}]')
        return "# " + ', '.join(self.comments)


