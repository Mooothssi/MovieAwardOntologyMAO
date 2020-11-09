from dataclasses import dataclass

from frogsql.base import BaseModel


@dataclass(eq=False)
class TitleBasics(BaseModel):
    _instances = []
    fields = (
        ('tconst', 'tconst', 'char(12)'),
        ('titleType', 'titleType', 'nvarchar(255)'),
        ('primaryTitle', None, 'nvarchar(255)'),
        ('originalTitle', None, 'nvarchar(255)'),
        ('isAdult', None, 'int'),
        ('startYear', None, 'int'),
        ('endYear', None, 'int'),
        ('runtimeMinutes', None, 'int'),
        ('genres', 'genres', 'nvarchar(255)'),
    )
    tconst: str = None
    titleType: str = None
    primaryTitle: str = None
    originalTitle: str = None
    isAdult: int = None
    startYear: int = None
    endYear: int = None
    runtimeMinutes: int = None
    genres: str = None

    def __post_init__(self):
        if self.endYear:
            if self.endYear == r'\N':
                self.endYear = None
        try:
            self.isAdult = int(self.isAdult)
        except ValueError or TypeError:
            self.isAdult = 0
