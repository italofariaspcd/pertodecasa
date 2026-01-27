from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações do seu projeto (mantive igual)
from database import engine, get_db, Base
from models import User, Category, Provider
from auth import get_password_hash
from pydantic import BaseModel

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configura a pasta de templates
templates = Jinja2Templates(directory="templates")

# --- ROTAS DE API (MANTIDAS) ---
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    is_provider: bool = False
    whatsapp: Optional[str] = None
    bio: Optional[str] = None
    category_ids: List[int] = []
    address_neighborhood: Optional[str] = None

@app.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        is_provider=user.is_provider
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.is_provider:
        new_provider = Provider(
            id=new_user.id,
            whatsapp=user.whatsapp,
            bio=user.bio,
            address_neighborhood=user.address_neighborhood
        )
        if user.category_ids:
            cats = db.query(Category).filter(Category.id.in_(user.category_ids)).all()
            new_provider.categories = cats
        
        db.add(new_provider)
        db.commit()

    return {"msg": "Usuário criado com sucesso"}

# --- NOVA ROTA VISUAL (WEB) ---
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, category_slug: Optional[str] = None, bairro: Optional[str] = None, db: Session = Depends(get_db)):
    # 1. Busca todas as categorias para preencher o dropdown
    categorias = db.query(Category).all()

    profissionais = []
    buscar_realizada = False

    # 2. Se o usuário selecionou uma categoria, faz a busca
    if category_slug:
        buscar_realizada = True
        query = db.query(Provider).join(Provider.categories).filter(Category.slug == category_slug)
        
        if bairro:
            query = query.filter(Provider.address_neighborhood.ilike(f"%{bairro}%"))
            
        providers = query.all()
        
        # Formata os dados para o HTML
        for p in providers:
            # Pega o nome do usuário associado
            user = db.query(User).filter(User.id == p.id).first()
            profissionais.append({
                "full_name": user.full_name,
                "whatsapp": p.whatsapp,
                "bio": p.bio,
                "address_neighborhood": p.address_neighborhood,
                "categories": p.categories
            })

    # 3. Renderiza o HTML com os dados
    return templates.TemplateResponse("index.html", {
        "request": request,
        "categorias": categorias,
        "profissionais": profissionais,
        "buscar_realizada": buscar_realizada,
        "categoria_selecionada": category_slug,
        "bairro_atual": bairro if bairro else ""
    })