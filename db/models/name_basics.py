
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKeyConstraint
from .base import BaseModel
from .title_basics import TitleBasics


class NameBasics(BaseModel):
    __tablename__ = "NameBasics"

    fields = (
        ('nconst', 'nconst', 'char(9)'),
        ('primaryName', None, 'nvarchar(255)'),
        ('birthYear', None, 'int'),
        ('deathYear', None, 'int'),
        ('primaryProfession', None, 'nvarchar(255)'),
        ('knownForTitles', None, 'nvarchar(255)'),
    )

    nconst: str = Column(
        String(9),
        nullable=False,
        primary_key=True
    )
    primaryName: str = Column(
        String,
        nullable=False
    )
    birthYear: int = Column(
        Integer,
        nullable=False
    )
    deathYear: int = Column(
        Integer,
        nullable=True
    )
    primaryProfession: str = Column(
        String,
        nullable=False
    )
    knownForTitles: str = Column(
        String,
        nullable=True
    )
    # region: str = None
    # language: str = None
    # types: str = None
    # attributes: str = None
    # isOriginalTitle: str = None

    def __repr__(self):
        return '<TitleAkas model {}>'.format(self.titleId)
