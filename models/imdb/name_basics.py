from dataclasses import dataclass

from frogsql.base import BaseModel

from .base import clean_backslash_n_multiple


@dataclass(eq=False)
class NameBasics(BaseModel):
    _instances = []
    fields = (
        ('nconst', 'nconst', 'char(9)'),
        ('primaryName', None, 'nvarchar(255)'),
        ('birthYear', None, 'int'),
        ('deathYear', None, 'int'),
        ('primaryProfession', None, 'nvarchar(255)'),
        ('knownForTitles', None, 'nvarchar(255)'),
    )

    nconst: str = None
    primaryname: str = None
    birthyear: int = None
    birthYear: int = None
    deathyear: int = None
    deathYear: int = None
    primaryProfession: str = None
    primaryprofession: str = None
    knownForTitles: str = None
    knownfortitles: str = None
