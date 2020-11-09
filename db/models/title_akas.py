
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel
from .title_basics import TitleBasics


class TitleAkas(BaseModel):
    __tablename__ = "TitleAkas"

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

    titleId: str = Column(
        String(9),
        nullable=False
    )
    ordering: int = Column(
        Integer,
        nullable=False
    )
    title: str = Column(
        String,
        nullable=False
    )
    region: str = Column(
        String,
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint('titleId', 'ordering'),
        ForeignKeyConstraint(name="akas_title_fk", refcolumns=[TitleBasics.titleId], columns=(titleId,)),
    )

    def __repr__(self):
        return '<TitleAkas model {}>'.format(self.titleId)
