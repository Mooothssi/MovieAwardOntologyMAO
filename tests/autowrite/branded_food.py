from sqlalchemy import Column, Integer, String, Date

from .base import Base


class Nutrient(Base):
    __tablename__ = 'nutrient'

    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)                     # unique: 10000, val = [356425,410933]
    brand_owner = Column(String)                 # unique: 2074, len = [2,65]
    gtin_upc = Column(String)                    # unique: 10000, len = {8,10,12,13}
    ingredients = Column(String)                 # unique: 8778, len = [0,2287], len(arr) = [1,109]
    serving_size = Column(Integer)               #
    serving_size_unit = Column(String)           #
    household_serving_fulltext = Column(String)  #
    branded_food_category = Column(String)       #
    data_source = Column(String)                 #
    modified_date = Column(Date)                 #
    available_date = Column(Date)                # unique: 10000, val = [2017-06-24, 2019-01-04]

    def __repr__(self):
        return f"<Nutrient(fdc_id='{self.fdc_id}' brand_owner='{self.brand_owner}' gtin_upc='{self.gtin_upc}' ingredients='{self.ingredients}' serving_size='{self.serving_size}' serving_size_unit='{self.serving_size_unit}' household_serving_fulltext='{self.household_serving_fulltext}' branded_food_category='{self.branded_food_category}' data_source='{self.data_source}' modified_date='{self.modified_date}' available_date='{self.available_date}')>"
