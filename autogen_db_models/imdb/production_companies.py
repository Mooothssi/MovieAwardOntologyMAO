import re

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
    country_code = Column(String)
    comment = Column(String)

    def __repr__(self):
        return f"<ProductionCompanies(id='{self.id}', title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episode_info ='{self.episode_info}', production_company='{self.production_company}', country_code='{self.country_code}', comment='{self.comment}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        m = re.match(r'(?P<production_company>.*) \[(?P<country_code>[a-z]+)\](\t(?P<comment>.*))?|(?P<prod_comp>.*)', row.get('data'))
        if m is None:
            raise ValueError(f"SOmE EROROR {row}")
        dct = m.groupdict()
        prod_comp = dct.get('production_company')
        if prod_comp is None:
            prod_comp = dct.get('prod_comp')
        assert prod_comp is not None
        cc = dct.get('country_code')
        comment = dct.get('comment')
        data = {
            'title': row.get('title'),
            'year': row.get('year'),
            'roman': row.get('roman'),
            'type': row.get('type'),
            'episode_info': row.get('episode_info'),
            'production_company': prod_comp,
            'country_code': cc,
            'comment': comment,
        }
        return cls(**data)
