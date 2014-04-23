from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, Float, String, PickleType

import settings

def db_connect():
    """
    Performs database connections using database settings from settings.py,
    Returns sqlalchemy engine instance
    """

    return create_engine(URL(**settings.DATABASE))

DeclarativeBase = declarative_base()

def create_frames_table(engine):

    DeclarativeBase.metadata.create_all(engine)

class Frames(DeclarativeBase):
    """
    sqlalchemy's db model for men's frames
    """

    __tablename__ = "frames"

    brand = Column('brand', String)
    url = Column(String, primary_key=True)
    colors = Column('colors', PickleType, nullable=True)
    price = Column('price', Float)
    retail_price = Column('retail price', Float)

