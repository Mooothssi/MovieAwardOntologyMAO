from typing import List, Dict, TypeVar, Iterable, Tuple, Any, Sequence, TextIO, Generator
from datetime import date, datetime, time
import warnings


class SQLWriter:
    def __init__(self, f: TextIO, dialect: str = "SQL Server", **kwargs):
        if dialect.lower() != 'sql server':
            raise NotImplementedError
        self.dialect = dialect.lower()
        self.dbtypes: List[str] = kwargs.pop('dbtypes', None)
        self.check: List[str] = kwargs.pop('check', True)
        self.f = f

    def escape_string(self, s: str) -> str:
        if "'" in s:
            if self.dialect == 'sql server':
                return s.replace("'", "''")
            else:
                return s.replace("'", r"\'")
        return s

    def convert_row(self, row: Iterable[Any]) -> str:
        lst = []

        if self.dbtypes is not None and self.check:
            # print(row)
            for datatype, value in zip(self.dbtypes, row):
                if value is None:
                    text = 'NULL'
                elif isinstance(datatype, str):
                    if datatype in ('int', 'tinyint', 'smallint', 'bigint'):
                        if not isinstance(value, int):
                            warnings.warn(repr(row))
                            warnings.warn(UserWarning(f"type mismatch '{value}' of class '{value.__class__.__name__}' --> '{datatype}'"))
                        if datatype == 'int':
                            if not -2_147_483_648 <= value <= 2_147_483_647:
                                warnings.warn(UserWarning(f"value '{value}' seems to be out of bound for datatype {datatype} ({-2_147_483_648},{2_147_483_647})"))
                            text = str(value)
                        elif datatype == 'tinyint':
                            if not 0 <= value <= 255:
                                warnings.warn(UserWarning(f"value '{value}' seems to be out of bound for datatype {datatype} ({0},{255})"))
                            text = str(value)
                        elif datatype == 'smallint':
                            if not -32_768 <= value <= 32_767:
                                warnings.warn(UserWarning(f"value '{value}' seems to be out of bound for datatype {datatype} ({-32_768},{32_767})"))
                            text = str(value)
                        elif datatype == 'bigint':
                            if not -9_223_372_036_854_775_808 <= value <= 9_223_372_036_854_775_807:
                                warnings.warn(UserWarning(f"value '{value}' seems to be out of bound for datatype {datatype} ({-9_223_372_036_854_775_808},{9_223_372_036_854_775_807})"))
                            text = str(value)
                        else:
                            raise AssertionError(f"What is this data type? '{datatype}'??? not supported")
                    elif datatype.startswith('decimal'):
                        if datatype == 'decimal':
                            # not specified
                            precision, scale = 18, 0
                        else:
                            assert datatype[7] == '(', datatype
                            assert datatype[-1] == ')', datatype
                            precision, scale = datatype[8:-1].split(',')
                            precision, scale = int(precision), int(scale)
                        text = str(value)
                        # TODO: check value is within bounds
                        front, back = text.split('.')
                        if len(back) > scale:
                            warnings.warn(f"value '{value}' seems to be out of bound of datatype {datatype}")
                            text = str(round(value, scale))
                            front, back = text.split('.')
                        if len(front + back) > precision:
                            raise ValueError(f"value '{value}' seems to be out of bound of datatype {datatype}")
                    elif datatype.startswith('varchar'):
                        assert datatype[7] == '(', datatype
                        assert datatype[-1] == ')', datatype
                        limit = int(datatype[8:-1])
                        if len(value) > limit:
                            warnings.warn(repr(row))
                            warnings.warn(f'str "{value}" exceeds the limit for {datatype}')
                        text = f"'{self.escape_string(value)}'"
                    elif datatype.startswith('nvarchar'):
                        assert datatype[8] == '(', datatype
                        assert datatype[-1] == ')', datatype
                        limit = int(datatype[9:-1])
                        if len(value) > limit:
                            print(row)
                            warnings.warn(f'str "{value}" exceeds the limit for {datatype}')
                        text = f"N'{self.escape_string(value)}'"
                    elif datatype == 'date':
                        text = f"'{value.year:04}-{value.month:02}-{value.day:02}'"
                    elif datatype == 'datetime':
                        text = f"'{value.year:04}-{value.month:02}-{value.day:02} {value.hour:02}:{value.minute:02}:{value.second:02}'"
                    elif datatype == 'time':
                        text = f"'{value.hour:02}:{value.minute:02}:{value.second:02}'"
                    else:
                        raise NotImplementedError(f"encoding for '{datatype}' not supported")
                else:
                    raise AssertionError(f"datatype must be a str not a '{datatype}'")
                lst.append(text)
        else:
            for i, value in enumerate(row):
                if value is None:
                    text = 'NULL'
                elif isinstance(value, int):
                    text = str(value)
                elif isinstance(value, float):
                    text = str(value)
                elif isinstance(value, str):
                    if value == '':
                        text = 'NULL'
                        lst.append(text)
                        continue
                    # escape single quotes
                    text = f"'{self.escape_string(value)}'"
                elif isinstance(value, date):
                    text = f"'{value.year:04}-{value.month:02}-{value.day:02}'"
                elif isinstance(value, datetime):
                    text = f"'{value.year:04}-{value.month:02}-{value.day:02} {value.hour:02}:{value.minute:02}:{value.second:02}'"
                elif isinstance(value, time):
                    text = f"'{value.hour:02}:{value.minute:02}:{value.second:02}'"
                else:
                    raise ValueError(f"value '{value}' of class '{value.__class__.__name__} 'is not of valid type")
                lst.append(text)
        return f"({','.join(lst)})"

    def writerow(self, row: Iterable[Any]):
        self.f.write(f"    {self.convert_row(row)},\n")

    def writerows(self, rows: Iterable[Iterable[Any]]):
        n = 0
        lst = []
        for row in rows:
            lst.append(self.convert_row(row))
            n += 1
        text = ',\n    '.join(lst)
        if n > 1000 and self.dialect == 'sql server':
            raise ValueError("The number of row value expressions in the INSERT statement exceeds the maximum allowed number of 1000 row values.")
        self.f.write(f'    {text};\n')

    def write_truncate(self, table_name: str):
        # self.f.write(f"IF OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL\n    DELETE FROM {table_name};\nGO\n")
        self.f.write(f"IF OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL\n    TRUNCATE TABLE {table_name};\nGO\n")

    def write_identity_insert(self, table_name: str, value: str = 'ON'):
        assert value.upper() in ('ON', 'OFF')
        self.f.write(f"SET IDENTITY_INSERT {table_name} {value.upper()};\n")

    def writeheader(self, table_name: str, cols: Iterable[str] = None):
        colstr = ''
        if cols is not None:
            colstr = f"({', '.join(f'[{col}]' for col in cols)}) "
        self.f.write(f'INSERT INTO {table_name} {colstr}VALUES\n')


class DictWriter:
    def __init__(self, f, fieldnames: Iterable[str], *, extrasaction: str = "raise",
                 dialect: str = "SQL Server", **kwargs):
        self.fieldnames = fieldnames    # list of keys for the dict
        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError("extrasaction (%s) must be 'raise' or 'ignore'"
                             % extrasaction)
        self.extrasaction = extrasaction.lower()
        self.writer = SQLWriter(f, dialect)

    def _dict_to_list(self, rowdict) -> Generator:
        if self.extrasaction == "raise":
            wrong_fields = rowdict.keys() - self.fieldnames
            if wrong_fields:
                raise ValueError("dict contains fields not in fieldnames: "
                                 + ", ".join([repr(x) for x in wrong_fields]))
        return (rowdict.get(key, 'NULL') for key in self.fieldnames)

    def writeheader(self, table_name: str):
        self.writer.writeheader(table_name)

    def writerow(self, rowdict):
        return self.writer.writerow(self._dict_to_list(rowdict))

    def writerows(self, rowdicts):
        return self.writer.writerows(map(self._dict_to_list, rowdicts))


def writetable(data: List[Dict], table_name: str, filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = DictWriter(file, data[0].keys())
        writer.writer.write_truncate(table_name)
        iterable = data.__iter__()
        while True:
            datab = []
            n = 0
            for row in iterable:
                datab.append(row)
                n += 1
                if n == 1000:
                    break
            if not datab:
                break
            writer.writeheader(table_name)
            writer.writerows(datab)
