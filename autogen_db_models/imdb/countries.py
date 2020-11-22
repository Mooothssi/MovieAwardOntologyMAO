from sqlalchemy import Column, Integer, String

from .base import Base


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episode_info = Column(String)
    country = Column(String)

    def __repr__(self):
        return f"<Countries(id='{self.id}', title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episode_info='{self.episode_info }', country='{self.country}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        data = {
            'title': row.get('title'),
            'year': row.get('year'),
            'roman': row.get('roman'),
            'type': row.get('type'),
            'episode_info': row.get('episode_info'),
            'country': row.get('data'),
        }
        return cls(**data)
