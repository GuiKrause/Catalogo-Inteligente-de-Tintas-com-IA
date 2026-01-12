from sqlalchemy import Column, Text, Boolean
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    id = Column[UUID](UUID[UUID](as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column[str](Text, unique=True, index=True)
    password = Column[str](Text)
    role = Column[str](Text, default="user")
    is_active = Column[bool](Boolean)