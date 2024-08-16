from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Personaje(Base):
    __tablename__ = 'personajes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    raza = Column(String(100), nullable=False)
    elemento = Column(String(100), nullable=False)
