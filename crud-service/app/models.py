from sqlalchemy import Column, Numeric, Text, Boolean, Enum
from pgvector.sqlalchemy import Vector
from .database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    id = Column[UUID](UUID[UUID](as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column[str](Text, unique=True, index=True)
    password = Column[str](Text)
    role = Column[str](Text, default="user")
    is_active = Column[bool](Boolean)


# Enums devem bater exatamente com o banco
tipo_tinta_enum = Enum(
    "Acrílica", "Látex", "Esmalte", "Epóxi", "Verniz",
    name="tipo_tinta_enum"
)

superficie_enum = Enum(
    "Parede", "Madeira", "Metal", "Piso", "Concreto",
    name="superficie_enum"
)

ambiente_enum = Enum(
    "Interno", "Externo", "Interno/Externo",
    name="ambiente_enum"
)

base_enum = Enum(
    "Água", "Solvente",
    name="base_enum"
)

acabamento_enum = Enum(
    "Fosca", "Acetinada", "Semibrilho", "Brilhante",
    name="acabamento_enum"
)

linha_enum = Enum(
    "Econômica", "Standard", "Premium",
    name="linha_enum"
)

nivel_odor_enum = Enum(
    "Baixo", "Médio", "Alto",
    name="nivel_odor_enum"
)


class Paint(Base):
    __tablename__ = "paints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nome = Column(Text, nullable=False)
    descricao = Column(Text)

    cor = Column(Text, nullable=False)

    tipo_tinta = Column(tipo_tinta_enum, nullable=False)
    superficie = Column(superficie_enum, nullable=False)
    ambiente = Column(ambiente_enum, nullable=False)
    base = Column(base_enum, nullable=False)
    acabamento = Column(acabamento_enum, nullable=False)
    linha = Column(linha_enum, nullable=False)
    nivel_odor = Column(nivel_odor_enum, nullable=False)

    rendimento_m2_l = Column(Numeric(5, 2))
    volume_l = Column(Numeric(6, 2))
    preco = Column(Numeric(10, 2), nullable=False)

    anti_mofo = Column(Boolean, default=False)
    lavavel = Column(Boolean, default=False)
    disponivel = Column(Boolean, default=True)

    embedding = Column(Vector(1536))