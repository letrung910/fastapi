from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_DEBUG


def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=SQLALCHEMY_DATABASE_DEBUG)
metadata = MetaData()

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
