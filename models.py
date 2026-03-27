from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    profissionais = relationship("Profissional", back_populates="categoria")

class Profissional(Base):
    __tablename__ = "profissionais"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String)
    redes_sociais = Column(String, nullable=True)
    endereco = Column(String)
    numero = Column(String)
    cidade = Column(String)
    descricao = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    ativo = Column(Boolean, default=True)
    is_destaque = Column(Boolean, default=False) # NOVO: Para o Carrossel

    categoria = relationship("Categoria", back_populates="profissionais")