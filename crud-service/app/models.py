from uuid import UUID


from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    id = Column[UUID](UUID[UUID](as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column[str](String, unique=True, index=True)
    password = Column[str](String)
    role = Column[str](String, default="user")
    is_active = Column[bool](Boolean)


class Paint(Base):
    __tablename__ = "paints"
    id = Column[int](Integer, primary_key=True, index=True)
    nome = Column[str](String)
    cor = Column[str](String)