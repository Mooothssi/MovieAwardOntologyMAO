from sqlalchemy import Column, Integer, String

from .base import Base


class Nutrient(Base):
    __tablename__ = 'nutrient'

    _id = Column(Integer, primary_key=True)
    id = Column(Integer)
    name = Column(String)
    unit_name = Column(String)
    nutrient_nbr = Column(Integer)
    rank = Column(Integer)

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}', unit_name='{self.unit_name}', nutrient_nbr='{self.nutrient_nbr}', rank='{self.rank}')>"
