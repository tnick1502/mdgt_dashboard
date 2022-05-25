from sqlalchemy import Column, Date, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)


class Report(Base):
    __tablename__ = 'reports'

    date = Column(Date, primary_key=True)
    python_report = Column(Integer)
    python_dynamic_report = Column(Integer)
    python_compression_report = Column(Integer)
    mathcad_report = Column(Integer)
    physical_statement = Column(Integer)
    mechanics_statement = Column(Integer)
    python_all = Column(Float)
    python_percent = Column(Float)


class Prize(Base):
    __tablename__ = 'prizes'

    date = Column(Date, primary_key=True)
    prize = Column(Float)
