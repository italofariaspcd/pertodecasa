from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabela de Associação (Muitos-para-Muitos)
provider_category = Table(
    'provider_category', Base.metadata,
    Column('provider_id', Integer, ForeignKey('providers.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_provider = Column(Boolean, default=False)
    
    provider_profile = relationship("Provider", uselist=False, back_populates="user")

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    whatsapp = Column(String)
    instagram = Column(String, nullable=True) # <--- NOVO CAMPO
    bio = Column(String)
    address_neighborhood = Column(String)
    
    user = relationship("User", back_populates="provider_profile")
    categories = relationship("Category", secondary=provider_category, back_populates="providers")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    slug = Column(String, unique=True)
    
    providers = relationship("Provider", secondary=provider_category, back_populates="categories")