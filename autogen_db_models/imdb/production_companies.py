from sqlalchemy import Column, Integer, String

from .base import Base


class ProductionCompanies(Base):
    __tablename__ = 'production_companies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episode_info = Column(String)
    production_company = Column(String)

    def __repr__(self):
        return f"<ProductionCompanies(id='{self.id}', title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episode_info ='{self.episode_info }', production_company='{self.production_company}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        data = {
            'title': row.get('title'),
            'year': row.get('year'),
            'roman': row.get('roman'),
            'type': row.get('type'),
            'episode_info': row.get('episode_info'),
            'production_company': row.get('data'),
        }
        return cls(**data)
