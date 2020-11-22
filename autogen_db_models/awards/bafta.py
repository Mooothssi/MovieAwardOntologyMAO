from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class Bafta(Base):
    __tablename__ = 'bafta'

    _id = Column(Integer, primary_key=True)  # unique: 4176, val = [0,4175]
    year = Column(Integer)                   # unique: 54, val = [1949,2020]
    category = Column(String)                # unique: 999, len = [19,125]
    nominee = Column(String)                 # unique: 2471, len = [1,102]
    workers = Column(String)                 # unique: 2520, len = [0,193]
    winner = Column(Boolean)                 # unique: 2, len = {4,5}

    def __repr__(self):
        return f"<Bafta(_id='{self._id}', year='{self.year}', category='{self.category}', nominee='{self.nominee}', workers='{self.workers}', winner='{self.winner}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        data = {
            'year': int(row.get('year')),
            'category': row.get('category'),
            'nominee': row.get('nominee'),
            'workers': row.get('workers'),
            'winner': row.get('winner'),
        }
        return cls(**data)
