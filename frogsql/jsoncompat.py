from __future__ import annotations

from dataclasses import is_dataclass
from datetime import datetime, date, time, timedelta
import json
import importlib


class Date(date):
    """
    Represents ``Date``.
    Adds JSON support to Python Standard Library ``datetime.Date``.

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Dates
    """
    def as_json(self) -> dict:
        d = {
            '@class': self.__class__.__name__,
            '@module': 'jsoncompat',
            'isoformat': self.isoformat()
        }
        return d

    @classmethod
    def from_json(cls, dct: dict) -> Date:
        return cls.fromisoformat(dct['isoformat'])


class Time(time):
    """
    Represents ``Time``.
    Adds JSON support to Python Standard Library ``datetime.Time``

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Times
    """
    def as_json(self) -> dict:
        d = {
            '@class': self.__class__.__name__,
            '@module': 'jsoncompat',
            'isoformat': self.isoformat()
        }
        return d

    @classmethod
    def from_json(cls, dct: dict) -> Time:
        return cls.fromisoformat(dct['isoformat'])


class DateTime(datetime, Date):
    """
    Represents ``DateTime``.
    Adds JSON support to Python Standard Library ``datetime.DateTime``

    References:
        https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations
    """
    def __str__(self):
        """
        Returns ISO 8601 format date

        # TODO: make tests
        """
        return super().isoformat()

    def as_json(self) -> dict:
        d = {
            '@class': self.__class__.__name__,
            '@module': 'jsoncompat',
            'isoformat': self.isoformat()
        }
        return d

    @classmethod
    def from_json(cls, dct: dict) -> DateTime:
        return cls.fromisoformat(dct['isoformat'])

    @classmethod
    def fromisoformat(cls, date_string: str) -> DateTime:
        """
        Args:
            date_string: The string to convert to DateTime
        """
        # noinspection PyTypeChecker
        return super().fromisoformat(date_string.replace('Z', '+00:00'))


class TimeDelta(timedelta):
    def as_json(self) -> dict:
        d = {
            '@class': self.__class__.__name__,
            '@module': 'jsoncompat',
            'days': self.days,
            'seconds': self.seconds,
            'microseconds': self.microseconds,
        }
        return d

    @classmethod
    def from_json(cls, dct: dict) -> TimeDelta:
        return cls(**dct)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'as_json'):
            return o.as_json()
        raise TypeError(f'Object of type {o.__class__.__name__} '
                        f'is not JSON serializable')


def hook(dct: dict):
    # dataclass
    if '@class' in dct:
        if '@module' in dct:
            module = importlib.import_module(dct.pop('@module'))
            cls = getattr(module, dct.pop('@class'))
            if hasattr(cls, 'from_json'):
                return cls.from_json(dct)
            try:
                return cls(**dct)
            except Exception as e:
                raise AssertionError("Implement from_json() or make sure the class can init from dict!") from e
        raise AssertionError("I don't know which module the class is in")
    return dct


class JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=hook, *args, **kwargs)


if __name__ == '__main__':
    # dt = TimeDelta(seconds=59, hours=2)
    # s = json.dumps(dt, cls=JSONEncoder)
    # print(json.loads(s, cls=JSONDecoder))

    from models.port import Port

    # port1 = Port(1, 'Salabun', 'Seaport', 'Big', '### ####', '123', '', '1234')
    # port2 = Port(123, 'Monaprom', 'Seaport', 'Large', '### ####', 'ppp', '', 'k')
    # print(port)
    # s = json.dumps(port, cls=JSONEncoder)
    # print(json.loads(s, cls=JSONDecoder))

    # Port.dump_to_csv('test.csv')
    # Port.load_from_csv('test.csv')

    print(Port.get_instance_by_key(2))


