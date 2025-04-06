import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_connection_string():
    dbengine = os.environ.get("DB_ENGINE", "postgresql")
    dbhost = os.environ.get("DB_HOST")
    dbport = os.environ.get("DB_PORT", "5432")
    dbusername = os.environ.get("DB_USERNAME")
    dbpassword = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")

    return f'{dbengine}://{dbusername}:{dbpassword}@{dbhost}:{dbport}/{dbname}'


SQLALCHEMY_DATABASE_URL = get_connection_string()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
