from dataclasses import dataclass

from frogsql.base import BaseModel


@dataclass(eq=False)
class TitlePrincipal(BaseModel):
    _instances = []
    fields = (
        ('tconst', 'tconst', 'char(9)'),
        ('ordering', None, 'int'),
        ('nconst', None, 'nvarchar(255)'),
        ('category', None, 'nvarchar(4)'),
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
        if self.job:
            if self.job == r'\N':
                self.job = None
        if self.characters:
            if self.characters == r'\N':
                self.characters = None
        # if self.types:
        #     if self.types == r'\N':
        #         self.types = None
        # if self.attributes:
        #     if self.attributes == r'\N':
        #         self.attributes = None
        # try:
        #     self.isOriginalTitle = int(self.isOriginalTitle)
        # except ValueError:
        #     self.isOriginalTitle = None
