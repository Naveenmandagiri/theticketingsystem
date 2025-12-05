import uuid

from db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import UUID

class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)