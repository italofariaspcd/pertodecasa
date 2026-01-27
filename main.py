from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações do seu projeto (Banco de Dados e Segurança)
from database import engine, get_db, Base
from models import User, Category, Provider
from auth import get_password_hash
from pydantic import BaseModel

# Cria as tabelas no banco se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configura a pasta onde estão os arquivos HTML
templates = Jinja2Templates(directory="templates")

# --- ROTA 1: PÁGINA INICIAL (BUSCA) ---
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, category_slug: Optional[str] = None, bairro: Optional[str] = None, db: Session = Depends(get_db)):
    # Busca categorias para o dropdown
    categorias = db.query(Category).all()
    profissionais = []
    buscar_realizada = False

    # Se tiver busca, filtra os profissionais
    if category_slug:
        buscar_realizada = True
        query = db.query(Provider).join(Provider.categories).filter(Category.slug == category_slug)
        
        if bairro:
            query = query.filter(Provider.address_neighborhood.ilike(f"%{bairro}%"))
            
        providers = query.all()
        
        # Monta os dados para exibir
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

# --- ROTA 2: PÁGINA DE CADASTRO (EXIBIR O FORMULÁRIO) ---
@app.get("/cadastro", response_class=HTMLResponse)
def view_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return templates.TemplateResponse("cadastro.html", {
        "request": request,
        "categorias": categorias
    })

# --- ROTA 3: RECEBER OS DADOS DO CADASTRO (SALVAR NO BANCO) ---
@app.post("/cadastro", response_class=HTMLResponse)
def submit_cadastro(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    whatsapp: str = Form(...),
    bio: str = Form(...),
    address_neighborhood: str = Form(...),
    category_ids: List[int] = Form([]), # Lista de IDs das categorias marcadas
    db: Session = Depends(get_db)
):
    categorias = db.query(Category).all()
    
    # 1. Verifica se o email já existe
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": "Eita! Esse e-mail já está cadastrado."
        })

    try:
        # 2. Cria o Usuário (Login)
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

        # 3. Cria o Perfil Profissional
        new_provider = Provider(
            id=new_user.id,
            whatsapp=whatsapp,
            bio=bio,
            address_neighborhood=address_neighborhood
        )
        
        # 4. Vincula as Categorias
        if category_ids:
            cats_db = db.query(Category).filter(Category.id.in_(category_ids)).all()
            new_provider.categories = cats_db
        
        db.add(new_provider)
        db.commit()

        # Retorna sucesso
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_sucesso": "Cadastro realizado com sucesso! Agora você aparece na busca."
        })

    except Exception as e:
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "categorias": categorias,
            "msg_erro": f"Erro no sistema: {str(e)}"
        })