from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

provider_category = Table(
    'provider_category', Base.metadata,
    Column('provider_id', Integer, ForeignKey('providers.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_provider = Column(Boolean, default=False)
    
    provider = relationship("Provider", back_populates="user", uselist=False)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    slug = Column(String, unique=True)
    
    # CORREÇÃO: Usando back_populates limpo, sem conflitos
    providers = relationship("Provider", secondary=provider_category, back_populates="categories")

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    whatsapp = Column(String)
    social_link = Column(String, nullable=True) 
    bio = Column(String)
    address_neighborhood = Column(String)
    is_vip = Column(Boolean, default=False) 

    user = relationship("User", back_populates="provider")
    
    # CORREÇÃO: Usando back_populates limpo, sem conflitos
    categories = relationship("Category", secondary=provider_category, back_populates="providers")