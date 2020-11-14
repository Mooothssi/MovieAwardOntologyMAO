from datetime import date, datetime
from typing import Any, Dict, List

from pandas import DataFrame, Series

from sa_autowrite.convenience import camel_to_snake
from sa_autowrite.date_utils import parse_date
from utils import select_not_null


def str_is_date(s: str) -> bool:
    """Check whether or not a string is a dat/"""
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


TYPE_CHECKER = {
    int: str.isnumeric,
    float: str.isdecimal,
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
    float: 'TODOOOOOOOO',
}


class Table:
    def __init__(self,
                 name: str,
                 data: DataFrame,
                 *,
                 gen_pk: bool = True,
                 pk_cols: List[str] = None):
        self.name = name  # Name of the table in CapWords
        self.data = data
        self.columns = []
        self.pk_cols = pk_cols
        for name in data.columns:
            col = Col(name)
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
                self.columns.insert(0, Col('_id', Series(range(len(self.data))), type_=int, is_pk=True))
            else:
                raise ValueError(f"Table '{self.name}' will have no primary key if not specified")
        else:
            for col in self.columns:
                if col.name in self.pk_cols:
                    col.is_pk = True

    def as_python(self) -> str:
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


class Col:
    def __init__(self, name: str, data: Series = None, *, type_: type = None, is_pk: bool = False):
        self.name = name
        self.data: Series = data
        self.type: type = type_
        self.is_pk = is_pk
        self.comments: List[str] = []

    def as_python(self, start: int = 55):
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


def write_model(filename: str,
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

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(table.as_python())


def write_base(filename: str):
    lines = [
        'from sqlalchemy.ext.declarative import declarative_base',
        '',
        'Base = declarative_base()',
        '',
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    from extended_csv import read_xsv_file
    write_base('base.py')
    write_model('branded_food.py', 'BrandedFood', read_xsv_file('../tests/data/csv/branded_food-10000.csv', dialect='excel'))


if __name__ == '__main__':
    main()
