from sqlalchemy import Column, Integer, String

from .base import Base


class TitleAkas(Base):
    __tablename__ = 'title_akas'

    # _id = Column(Integer, )                       # unique: 10000, val = [0,9999]
    titleId = Column(String, primary_key=True)    # unique: 4421, len = {9}
    ordering = Column(Integer, primary_key=True)  # unique: 41, val = [1,41]
    title = Column(String)                        # unique: 8113, len = [2,138]
    region = Column(String)                       # unique: 44, len = {2,3,4}
    language = Column(String)                     # unique: 16, len = {2,3}
    types = Column(String)                        # unique: 9, len = {2,3,5,7,8,11}
    attributes = Column(String)                   # unique: 40, len = [2,36]
    isOriginalTitle = Column(Integer)             # unique: 2, val = [0,1]

    def __repr__(self):
        return f"<TitleAkas(titleId='{self.titleId}', ordering='{self.ordering}', title='{self.title}', region='{self.region}', language='{self.language}', types='{self.types}', attributes='{self.attributes}', isOriginalTitle='{self.isOriginalTitle}')>"
