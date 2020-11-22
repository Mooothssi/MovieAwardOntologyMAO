from sqlalchemy import Column, Float, Integer, String

from .base import Base


class TitleRatings(Base):
    __tablename__ = 'title_ratings'

    # _id = Column(Integer)                      # unique: 10000, val = [0,9999]
    tconst = Column(String, primary_key=True)  # unique: 10000, len = {9}
    averageRating = Column(Float)              # unique: 84, val = [1.0,9.7]
    numVotes = Column(Integer)                 # unique: 1391, val = [5,164537]

    def __repr__(self):
        return f"<TitleRatings(tconst='{self.tconst}', averageRating='{self.averageRating}', numVotes='{self.numVotes}')>"
