from sqlalchemy import Column, Integer, String

from .base import Base


class ProductionCompanies(Base):
    __tablename__ = 'production_companies'

    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episodeInfo = Column(String)
    productionCompany = Column(String)

    def __repr__(self):
        return f"<ProductionCompanies(title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episodeInfo='{self.episodeInfo}', productionCompany='{self.productionCompany}')>"

