from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class Oscar(Base):
    __tablename__ = 'oscar'

    _id = Column(Integer, primary_key=True)  # unique: 10395, val = [0,10394]
    year_film = Column(Integer)              # unique: 92, val = [1927,2019]
    year_ceremony = Column(Integer)          # unique: 92, val = [1928,2020]
    ceremony = Column(Integer)               # unique: 92, val = [1,92]
    category = Column(String)                # unique: 111, len = [5,137]
    name = Column(String)                    # unique: 6666, len = [3,280]
    film = Column(String)                    # unique: 4834, len = [0,82]
    winner = Column(Boolean)                 # unique: 2, len = {4,5}

    def __repr__(self):
        return f"<Oscar(_id='{self._id}', year_film='{self.year_film}', year_ceremony='{self.year_ceremony}', ceremony='{self.ceremony}', category='{self.category}', name='{self.name}', film='{self.film}', winner='{self.winner}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        data = {
            'year_film': int(row.get('year_film')),
            'year_ceremony': int(row.get('year_ceremony')),
            'ceremony': int(row.get('ceremony')),
            'category': row.get('category'),
            'name': row.get('name'),
            'film': row.get('film'),
            'winner': row.get('winner'),
        }
        return cls(**data)
