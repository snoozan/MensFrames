from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, Float, String, PickleType
from sqlalchemy import scoped_session, sessionmaker

import settings

def db_connect():
    """
    Performs database connections using database settings from settings.py,
    Returns sqlalchemy engine instance
    """

    return create_engine(URL(**settings.DATABASE))

DeclarativeBase = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtention()))

def create_frames_table(engine):

    DeclarativeBase.metadata.create_all(engine)

class FramesURL(DeclarativeBase):
    """
    sqlalchemy's db model for men's frames
    """

    __tablename__ = "frames_url"

    url = Column(String, primary_key=True)

class FramesInfo(DeclarativeBase):

    __tablename__ = "frames_info"

    url = Column(String, primary_key=True)
    brand = Column(String)
    product_name = Column(String)
    product_img = Column(String)
    price = Column(Integer)
    color = Column(PickleType)


