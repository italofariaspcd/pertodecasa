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
    cidade = Column(String, default="Capela")
    descricao = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    # Controle da taxa de R$ 20,00
    aceitou_taxa = Column(Boolean, default=True)
    ativo = Column(Boolean, default=True) 

    categoria = relationship("Categoria", back_populates="profissionais")