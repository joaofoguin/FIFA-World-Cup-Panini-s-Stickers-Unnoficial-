from sqlalchemy import Column, Integer, String
from .database import Base


class Figurinha(Base):
    __tablename__ = "figurinhas"

    id = Column(Integer, primary_key=True, index=True)
    numero_album = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    pais = Column(String, nullable=False)