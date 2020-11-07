from settings import DB_NAME, DB_PASSWORD, DB_DRIVER, DB_USERNAME, DB_HOST
from sqlalchemy import create_engine
CONNECTION_STRING = f"mysql+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


def connect_database():
    engine = create_engine(CONNECTION_STRING)
    engine.connect()
