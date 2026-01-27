# Arquivo: schemas.py

from pydantic import BaseModel
from typing import List, Optional

# --- Schemas Básicos ---
class CategoryBase(BaseModel):
    id: int
    name: str
    slug: str
    group: str
    class Config:
        from_attributes = True  # <--- MUDOU AQUI (Era orm_mode)

class AddressBase(BaseModel):
    neighborhood: str
    city: str
    state: str

# --- Cadastro (Input) ---
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    is_provider: bool = False

    # Campos opcionais se for prestador
    whatsapp: Optional[str] = None
    bio: Optional[str] = None
    category_ids: Optional[List[int]] = []
    address_neighborhood: Optional[str] = None 

# --- Respostas (Output) ---
class ProviderListDTO(BaseModel):
    full_name: str
    whatsapp: str
    bio: str
    neighborhood: str
    categories: List[str] 
    
    class Config:
        from_attributes = True # <--- MUDOU AQUI TAMBÉM