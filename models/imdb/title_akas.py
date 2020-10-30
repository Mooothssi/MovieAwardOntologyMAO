from dataclasses import dataclass

from frogsql.base import BaseModel


@dataclass(eq=False)
class TitleAkas(BaseModel):
    _instances = []
    fields = (
        ('titleId', 'titleId', 'char(9)'),
        ('ordering', None, 'int'),
        ('title', None, 'nvarchar(255)'),
        ('region', None, 'nvarchar(4)'),
        ('language', None, 'nvarchar(3)'),
        ('types', None, 'nvarchar(20)'),
        ('attributes', None, 'nvarchar(255)'),
        ('isOriginalTitle', 'isOriginalTitle', 'int'),
    )

    titleId: str = None
    ordering: int = None
    title: str = None
    region: str = None
    language: str = None
    types: str = None
    attributes: str = None
    isOriginalTitle: str = None

    def __post_init__(self):
        if self.language:
            if self.language == r'\N':
                self.language = None
        if self.region:
            if self.region == r'\N':
                self.region = None
        if self.types:
            if self.types == r'\N':
                self.types = None
        if self.attributes:
            if self.attributes == r'\N':
                self.attributes = None
        try:
            self.isOriginalTitle = int(self.isOriginalTitle)
        except ValueError:
            self.isOriginalTitle = None
