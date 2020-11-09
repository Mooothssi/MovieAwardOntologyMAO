from dataclasses import dataclass
from .base import clean_backslash_n_multiple
from frogsql.base import BaseModel


@dataclass(eq=False)
class TitlePrincipal(BaseModel):
    _instances = []
    fields = (
        ('tconst', 'tconst', 'char(9)'),
        ('ordering', None, 'int'),
        ('nconst', None, 'nvarchar(255)'),
        ('category', None, 'nvarchar(20)'),
        ('job', None, 'nvarchar(50)'),
        ('characters', None, 'nvarchar(255)'),
    )

    tconst: str = None
    ordering: int = None
    nconst: str = None
    category: str = None
    job: str = None
    characters: str = None

    def __post_init__(self):
        clean_backslash_n_multiple(self, ["job", "characters", "category"])
