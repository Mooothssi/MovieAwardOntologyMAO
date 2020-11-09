from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db.models import BaseModel
from settings import (DB_DIALECT, DB_DRIVER, DB_HOST, DB_NAME, DB_PASSWORD,
                      DB_USERNAME)

from .models.title_principals import TitlePrincipal

if DB_DIALECT == "mssql":
    CONNECTION_STRING = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
else:
    CONNECTION_STRING = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?driver=SQL+Server+Native+Client+10.0"


def connect_database() -> Session:
    engine = create_engine(CONNECTION_STRING, connect_args={'database': DB_NAME})
    engine.connect()
    current_session = sessionmaker(bind=engine)()
    BaseModel.metadata.create_all(bind=engine)
    # TitlePrincipal.__table__.create(bind=engine)
    return current_session

