from sqlalchemy import Column, Integer, String

from .base import Base


class TitleEpisode(Base):
    __tablename__ = 'title_episode'

    _id = Column(Integer)                      # unique: 10000, val = [0,9999]
    tconst = Column(String, primary_key=True)  # unique: 10000, len = {9}
    parentTconst = Column(String)              # unique: 1502, len = {9,10}
    seasonNumber = Column(String)              # unique: 53, len = {1,2,4}
    episodeNumber = Column(String)             # unique: 595, len = {1,2,3,4}

    def __repr__(self):
        return f"<TitleEpisode(tconst='{self.tconst}', parentTconst='{self.parentTconst}', seasonNumber='{self.seasonNumber}', episodeNumber='{self.episodeNumber}')>"
