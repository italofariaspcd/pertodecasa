from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# Tabela associativa (Muitos-para-Muitos)
provider_categories = Table('provider_categories', Base.metadata,
    Column('provider_id', Integer, ForeignKey('providers.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_provider = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    address = relationship("Address", back_populates="user", uselist=False)
    provider_profile = relationship("Provider", back_populates="user", uselist=False)

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    street = Column(String)
    neighborhood = Column(String, index=True) # Ex: "Augusto Franco"
    city = Column(String, default="Aracaju")
    state = Column(String, default="SE")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    user = relationship("User", back_populates="address")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    slug = Column(String, unique=True, index=True)
    group = Column(String)
    icon = Column(String, nullable=True)

    providers = relationship("Provider", secondary=provider_categories, back_populates="categories")

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    whatsapp = Column(String)
    bio = Column(Text)
    is_verified = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="provider_profile")
    categories = relationship("Category", secondary=provider_categories, back_populates="providers")