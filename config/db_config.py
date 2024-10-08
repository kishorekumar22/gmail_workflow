from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# All the databases configurations goes in here, contains the db sessions and engines.

engine = create_engine("sqlite:///emails_automator.sqlite")
conn = engine.connect()


class Base(DeclarativeBase):
    pass

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
db_session = Session()
