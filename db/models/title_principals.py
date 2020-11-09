
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import BaseModel

from .title_basics import TitleBasics
from .name_basics import NameBasics


class TitlePrincipal(BaseModel):
    __tablename__ = "TitlePrincipal"
    fields = (
        ('tconst', 'tconst', 'char(9)'),
        ('ordering', None, 'int'),
        ('nconst', None, 'nvarchar(255)'),
        ('category', None, 'nvarchar(4)'),
        ('job', None, 'nvarchar(12)'),
        ('characters', None, 'nvarchar(255)'),
    )

    tconst: str = Column(
        String(9),
        nullable=False
    )
    ordering: int = Column(
        Integer,
        nullable=False
    )
    nconst: str = Column(
        String,
        nullable=False
    )
    category: str = Column(
        String,
        nullable=False
    )
    job: str = Column(
        String
    )
    characters: str = Column(
        String
    )

    name = relationship("NameBasics")

    __table_args__ = (
        PrimaryKeyConstraint('tconst', 'ordering', name='prin_pk'),
        ForeignKeyConstraint(name="titleId_fk", refcolumns=[TitleBasics.titleId], columns=(tconst,)),
        ForeignKeyConstraint(name="nconst_fk", refcolumns=[NameBasics.nconst], columns=(nconst,)),
    )

    def __repr__(self):
        return '<TitlePrincipal model {}>'.format(self.tconst)
