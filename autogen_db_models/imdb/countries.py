from sqlalchemy import Column, Integer, String

from .base import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episodeInfo = Column(String)
    country = Column(String)

    def __repr__(self):
        return f"<Countries(id='{self.id}', title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episodeInfo='{self.episodeInfo}', country='{self.country}')>"

