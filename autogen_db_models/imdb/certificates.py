from sqlalchemy import Column, Integer, String

from .base import Base


class Certificates(Base):
    __tablename__ = 'certificates'

    title = Column(String)
    year = Column(Integer)
    roman = Column(String)
    type = Column(String)
    episodeInfo = Column(String)
    certificate = Column(String)

    def __repr__(self):
        return f"<Certificates(title='{self.title}', year='{self.year}', roman='{self.roman}', type='{self.type}', episodeInfo='{self.episodeInfo}', certificate='{self.certificate}')>"

