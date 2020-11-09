from dataclasses import dataclass
from frogsql.base import BaseModel


@dataclass(eq=False)
class TitleCrew(BaseModel):
    _instances = []
    fields = (
        ('tconst', 'tconst', 'char(9)'),
        ('directors', None, 'nvarchar(255)'),
        ('writers', None, 'nvarchar(255)')
    )

    tconst: str = None
    directors: str = None
    writers: str = None

    def __post_init__(self):
        pass
