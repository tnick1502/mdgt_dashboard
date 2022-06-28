from sqlalchemy import Column, Date, Float, String, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    phone_number = Column(BigInteger, unique=True)
    sex = Column(String)
    email = Column(String, unique=True)
    birthday = Column(Date)
    organization = Column(String)
    level = Column(String)
