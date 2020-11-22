from sqlalchemy import Column, Integer, String

from .base import Base


class Certificates(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episode_info = Column(String)
    certificate = Column(String)

    def __repr__(self):
        return f"<Certificates(id='{self.id}', title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episode_info ='{self.episode_info }', certificate='{self.certificate}')>"

    @classmethod
    def create_instance(cls, row: 'Series'):
        data = {
            'title': row.get('title'),
            'year': row.get('year'),
            'roman': row.get('roman'),
            'type': row.get('type'),
            'episode_info ': row.get('episode_info'),
            'certificate': row.get('data'),
        }
        return cls(**data)