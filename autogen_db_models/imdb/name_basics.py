from sqlalchemy import Column, Integer, String

from .base import Base


class NameBasics(Base):
    __tablename__ = 'name_basics'

    # _id = Column(Integer)                      # unique: 10000, val = [0,9999]
    nconst = Column(String, primary_key=True)  # unique: 10000, len = {9}
    primaryName = Column(String)               # unique: 9880, len = [3,35]
    birthYear = Column(String)                 # unique: 164, len = {2,4}
    deathYear = Column(String)                 # unique: 131, len = {2,4}
    primaryProfession = Column(String)         # unique: 1552, len = [0,63]
    knownForTitles = Column(String)            # unique: 9926, len = [2,42]

    def __repr__(self):
        return f"<NameBasics(nconst='{self.nconst}', primaryName='{self.primaryName}', birthYear='{self.birthYear}', deathYear='{self.deathYear}', primaryProfession='{self.primaryProfession}', knownForTitles='{self.knownForTitles}')>"
