from sqlalchemy import Column, Integer, String

from .base import Base


class TitleCrew(Base):
    __tablename__ = 'title_crew'

    # _id = Column(Integer)                      # unique: 10000, val = [0,9999]
    tconst = Column(String, primary_key=True)  # unique: 10000, len = {9}
    directors = Column(String)                 # unique: 1419, len = {2,9,10,19,29,39,59,69}
    writers = Column(String)                   # unique: 3751, len = [2,189]

    def __repr__(self):
        return f"<TitleCrew(tconst='{self.tconst}', directors='{self.directors}', writers='{self.writers}')>"
