from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clients(Base):

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idnumber = Column(Integer, unique=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(Integer)
    address = Column(String)
    startdate = Column(Date, nullable=True)
    enddate   = Column(Date, nullable=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Client_users(Base):

    __tablename__ = 'client_users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    client_id = Column(Integer, index=True)

class Client_contracts(Base):
    __tablename__ = "client_contracts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, index=True)
    startdate = Column(Date, nullable=True)
    enddate = Column(Date, nullable=True)
    hours = Column(Integer)
    frequency = Column(Integer)
    status = Column(Boolean, default=True)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())