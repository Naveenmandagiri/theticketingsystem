import uuid

from db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import UUID

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)