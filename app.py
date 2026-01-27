from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações do seu projeto
from database import engine, get_db, Base
from models import User, Category, Provider
from auth import get_password_hash
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- ROTAS WEB (FRONTEND) ---

# 1. Página Inicial (Busca)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, category_slug: Optional[str] = None, bairro: Optional[str] = None, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    profissionais = []
    buscar_realizada = False

    if category_slug:
        buscar_realizada = True
        query = db.query(Provider).join(Provider.categories).filter(Category.slug == category_slug)
        if bairro:
            query = query.filter(Provider.address_neighborhood.ilike(f"%{bairro}%"))
        
        providers = query.all()
        for p in providers:
            user = db.query(User).filter(User.id == p.id).first()
            profissionais.append({
                "full_name": user.full_name,
                "whatsapp": p.whatsapp,
                "bio": p.bio,
                "address_neighborhood": p.address_neighborhood,
                "categories": p.categories
            })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "categorias": categorias,
        "profissionais": profissionais,
        "buscar_realizada": buscar_realizada,
        "categoria_selecionada": category_slug,
        "bairro_atual": bairro if bairro else ""
    })

# 2. Página de Cadastro (Exibir Formulário)
@app.get("/cadastro", response_class=HTMLResponse)
def view_cadastro(request: Request, db: Session = Depends(get_db)):
    # Buscamos as categorias para mostrar os checkboxes
    categorias = db.query(Category).all()
    return templates.TemplateResponse("cadastro.html", {
        "request": request,
        "categorias": categorias
    })

# 3. Processar Cadastro (Receber Dados do Formulário)
@app.post("/cadastro", response_class=HTMLResponse)
def submit_cadastro(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    whatsapp: str = Form(...),
    bio: str = Form(...),
    address_neighborhood: str = Form(...),
    category_ids: List[int] = Form([]), # Recebe lista de IDs marcados
    db: Session = Depends(get_db)
):
    categorias = db.query(Category).all()
    
    # Verifica se email já existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": "Esse e-mail já está cadastrado!"
        })

    try:
        # 1. Cria Usuário
        hashed_pwd = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_pwd,
            full_name=full_name,
            is_provider=True # Quem se cadastra por aqui é profissional
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 2. Cria Perfil Profissional
        new_provider = Provider(
            id=new_user.id,
            whatsapp=whatsapp,
            bio=bio,
            address_neighborhood=address_neighborhood
        )
        
        # 3. Vincula Categorias
        if category_ids:
            cats_db = db.query(Category).filter(Category.id.in_(category_ids)).all()
            new_provider.categories = cats_db
        
        db.add(new_provider)
        db.commit()

        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_sucesso": "Cadastro realizado com sucesso! Bem-vindo(a) ao time."
        })

    except Exception as e:
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": f"Erro interno: {str(e)}"
        })

# --- ROTAS API (JSON) - Mantidas para uso futuro ---
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    is_provider: bool = False
    whatsapp: Optional[str] = None
    bio: Optional[str] = None
    category_ids: List[int] = []
    address_neighborhood: Optional[str] = None

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@app.get("/search/{category_slug}")
def search_providers(category_slug: str, bairro: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Provider).join(Provider.categories).filter(Category.slug == category_slug)
    if bairro:
        query = query.filter(Provider.address_neighborhood.ilike(f"%{bairro}%"))
    providers = query.all()
    results = []
    for p in providers:
        user = db.query(User).filter(User.id == p.id).first()
        results.append({
            "full_name": user.full_name,
            "whatsapp": p.whatsapp,
            "bio": p.bio,
            "neighborhood": p.address_neighborhood,
            "categories": [c.name for c in p.categories]
        })
    return results