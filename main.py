from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações do projeto
from database import engine, get_db, Base
from models import User, Category, Provider
from auth import get_password_hash

# Cria as tabelas novas (lembre de ter deletado o .db antigo)
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- ROTA 1: BUSCA (HOME) ---
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
                "instagram": p.instagram, # <--- Enviando Instagram para o HTML
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

# --- ROTA 2: VER FORMULÁRIO DE CADASTRO ---
@app.get("/cadastro", response_class=HTMLResponse)
def view_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return templates.TemplateResponse("cadastro.html", {
        "request": request,
        "categorias": categorias
    })

# --- ROTA 3: PROCESSAR CADASTRO ---
@app.post("/cadastro", response_class=HTMLResponse)
def submit_cadastro(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    whatsapp: str = Form(...),
    instagram: Optional[str] = Form(None), # <--- Recebe o Insta (pode ser vazio)
    bio: str = Form(...),
    address_neighborhood: str = Form(...),
    category_ids: List[int] = Form([]),
    db: Session = Depends(get_db)
):
    categorias = db.query(Category).all()
    
    # Validação de Email Duplicado
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": "Esse e-mail já possui cadastro!"
        })

    # Limpeza do Instagram (Tira o @ se a pessoa colocou)
    insta_clean = instagram
    if insta_clean and insta_clean.startswith("@"):
        insta_clean = insta_clean.replace("@", "")
    if insta_clean == "": # Se deixou vazio
        insta_clean = None

    try:
        # 1. Cria Usuário
        hashed_pwd = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_pwd,
            full_name=full_name,
            is_provider=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 2. Cria Perfil Profissional
        new_provider = Provider(
            id=new_user.id,
            whatsapp=whatsapp,
            instagram=insta_clean, # <--- Salva no Banco
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
            "msg_sucesso": "Cadastro realizado com sucesso! Bem-vindo(a)!"
        })

    except Exception as e:
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": f"Erro interno: {str(e)}"
        })