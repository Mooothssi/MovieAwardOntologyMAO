from sqlalchemy import Column, String, ForeignKeyConstraint
from .base import BaseModel
from .title_basics import TitleBasics


class TitleCrew(BaseModel):
    __tablename__ = "TitleCrew"
    fields = (
        ('tconst', 'tconst', 'char(9)'),
        ('directors', None, 'nvarchar(255)'),
        ('writers', None, 'nvarchar(255)')
    )

    tconst: str = Column(
        String(9),
        primary_key=True,
        nullable=False
    )
    directors: str = Column(
        String,
        nullable=False
    )
    writers: str = Column(
        String,
        nullable=False
    )

    __table_args__ = (
        ForeignKeyConstraint(name="tconst_fk", refcolumns=[TitleBasics.titleId], columns=(tconst,)),
    )

    def __repr__(self):
        return '<TitleCrew model {}>'.format(self.tconst)
