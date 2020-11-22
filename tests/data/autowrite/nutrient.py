from sqlalchemy import Column, Integer, String

from .base import Base


class Nutrient(Base):
    __tablename__ = 'nutrient'

    id = Column(Integer, primary_key=True)  # unique: 100, val = [1002,1191]
    name = Column(String)                   # unique: 99, len = [3,34]
    unit_name = Column(String)              # unique: 8, len = {1,2,4,5,6}
    nutrient_nbr = Column(String)           # unique: 100, len = {3,5}
    rank = Column(String)                   # unique: 92, len = {0,3,4,5,6}

    def __repr__(self):
        return f"<Nutrient(id='{self.id}', name='{self.name}', unit_name='{self.unit_name}', nutrient_nbr='{self.nutrient_nbr}', rank='{self.rank}')>"
