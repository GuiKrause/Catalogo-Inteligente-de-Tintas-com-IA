from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str


class Config:
    from_attributes = True


class PaintCreate(BaseModel):
    nome: str
    cor: str


class PaintOut(PaintCreate):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None