from sqlalchemy import Column, Integer, String

from .base import Base


class TitleBasics(Base):
    __tablename__ = 'title_basics'

    # _id = Column(Integer)                      # unique: 10000, val = [0,9999]
    tconst = Column(String, primary_key=True)  # unique: 10000, len = {9}
    titleType = Column(String)                 # unique: 2, len = {5}
    primaryTitle = Column(String)              # unique: 9625, len = [2,114]
    originalTitle = Column(String)             # unique: 9651, len = [2,114]
    isAdult = Column(Integer)                  # unique: 1, val = [0,0]
    startYear = Column(Integer)                # unique: 33, val = [1892,1936]
    endYear = Column(String)                   # unique: 1, len = {2}
    runtimeMinutes = Column(String)            # unique: 152, len = {1,2,3,4}
    genres = Column(String)                    # unique: 272, len = [2,27]

    def __repr__(self):
        return f"<tconst='{self.tconst}', titleType='{self.titleType}', primaryTitle='{self.primaryTitle}', originalTitle='{self.originalTitle}', isAdult='{self.isAdult}', startYear='{self.startYear}', endYear='{self.endYear}', runtimeMinutes='{self.runtimeMinutes}', genres='{self.genres}')>"
