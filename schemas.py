from pydantic import BaseModel
from typing import List, Optional

# --- Schemas Básicos ---
class CategoryBase(BaseModel):
    id: int
    name: str
    slug: str
    group: str
    class Config:
        orm_mode = True

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
    category_ids: Optional[List[int]] = [] # IDs das categorias que ele atende
    address_neighborhood: Optional[str] = None # Bairro para cadastro rápido

# --- Respostas (Output) ---
class ProviderListDTO(BaseModel):
    full_name: str
    whatsapp: str
    bio: str
    neighborhood: str
    categories: List[str] # Lista de nomes das categorias
    
    class Config:
        orm_mode = True