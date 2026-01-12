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

# Paints
class PaintBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cor: str

    tipo_tinta: str
    superficie: str
    ambiente: str
    base: str
    acabamento: str
    linha: str
    nivel_odor: str

    rendimento_m2_l: Optional[float] = None
    volume_l: Optional[float] = None
    preco: float

    anti_mofo: bool = False
    lavavel: bool = False
    disponivel: bool = True


class PaintCreate(PaintBase):
    pass


class PaintResponse(PaintBase):
    id: UUID
    nome: str

    class Config:
        from_attributes = True


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None