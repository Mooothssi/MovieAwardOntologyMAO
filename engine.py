from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dirs import ROOT_DIR

engine = create_engine(f"sqlite:///{ROOT_DIR / 'db.sqlite3'}")
Session = sessionmaker(bind=engine)
