from sqlalchemy import Column, Date, Integer, String

from .base import Base


class BrandedFood(Base):
    __tablename__ = 'branded_food'

    _id = Column(Integer, primary_key=True)      # unique: 10000, val = [0,9999]
    fdc_id = Column(Integer)                     # unique: 10000, val = [356425,410933]
    brand_owner = Column(String)                 # unique: 2074, len = [2,65]
    gtin_upc = Column(String)                    # unique: 10000, len = {8,10,12,13}
    ingredients = Column(String)                 # unique: 8778, len = [0,2287], len(arr) = [1,109]
    serving_size = Column(String)                # unique: 303, len = {1,2,3,4,5,6}
    serving_size_unit = Column(String)           # unique: 2, len = {1,2}
    household_serving_fulltext = Column(String)  # unique: 862, len = [0,75]
    branded_food_category = Column(String)       # unique: 117, len = [4,49]
    data_source = Column(String)                 # unique: 1, len = {2}
    modified_date = Column(Date)                 # unique: 397, val = [2017-06-24,2019-01-04]
    available_date = Column(Date)                # unique: 397, val = [2017-06-24,2019-01-04]

    def __repr__(self):
        return f"<BrandedFood(_id='{self._id}', fdc_id='{self.fdc_id}', brand_owner='{self.brand_owner}', gtin_upc='{self.gtin_upc}', ingredients='{self.ingredients}', serving_size='{self.serving_size}', serving_size_unit='{self.serving_size_unit}', household_serving_fulltext='{self.household_serving_fulltext}', branded_food_category='{self.branded_food_category}', data_source='{self.data_source}', modified_date='{self.modified_date}', available_date='{self.available_date}')>"
