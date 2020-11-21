from sqlalchemy import Column, Integer, String

from .base import Base


class TitlePrincipals(Base):
    __tablename__ = 'title_principals'

    _id = Column(Integer, primary_key=True)  # unique: 10000, val = [0,9999]
    tconst = Column(String)                  # unique: 2091, len = {9}
    ordering = Column(Integer)               # unique: 10, val = [1,10]
    nconst = Column(String)                  # unique: 1975, len = {9,10}
    category = Column(String)                # unique: 10, len = {4,5,6,7,8,15,19}
    job = Column(String)                     # unique: 103, len = [2,98]
    characters = Column(String)              # unique: 3632, len = [2,66]

    def __repr__(self):
        return f"<TitlePrincipals(_id='{self._id}', tconst='{self.tconst}', ordering='{self.ordering}', nconst='{self.nconst}', category='{self.category}', job='{self.job}', characters='{self.characters}')>"
