from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, get_db, Base
from models import User, Category, Provider

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, category_slug: Optional[str] = None, bairro: Optional[str] = None, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    profissionais = []
    buscar_realizada = False

    if category_slug:
        buscar_realizada = True
        query = db.query(Provider).join(Provider.categories)\
                  .filter(Category.slug == category_slug)\
                  .order_by(Provider.is_vip.desc(), Provider.address_neighborhood.asc())
        
        if bairro:
            query = query.filter(Provider.address_neighborhood.ilike(f"%{bairro}%"))
            
        providers = query.all()
        
        for p in providers:
            user = db.query(User).filter(User.id == p.id).first()
            profissionais.append({
                "id": p.id,
                "full_name": user.full_name,
                "whatsapp": p.whatsapp,
                "social_link": p.social_link,
                "bio": p.bio,
                "address_neighborhood": p.address_neighborhood,
                "categories": p.categories,
                "is_vip": p.is_vip
            })

    return templates.TemplateResponse("index.html", {
        "request": request, "categorias": categorias, "profissionais": profissionais,
        "buscar_realizada": buscar_realizada, "categoria_selecionada": category_slug, "bairro_atual": bairro if bairro else ""
    })

@app.get("/cadastro", response_class=HTMLResponse)
def view_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": categorias})

@app.post("/cadastro", response_class=HTMLResponse)
def submit_cadastro(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    whatsapp: str = Form(...),
    social_link: str = Form(""), 
    bio: str = Form(...),
    address_neighborhood: str = Form(...),
    category_ids: List[int] = Form([]),
    db: Session = Depends(get_db)
):
    categorias = db.query(Category).all()
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("cadastro.html", {
            "request": request, "categorias": categorias, "msg_erro": "Email já cadastrado!"
        })

    try:
        new_user = User(email=email, full_name=full_name, is_provider=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_provider = Provider(
            id=new_user.id, 
            whatsapp=whatsapp, 
            social_link=social_link, 
            bio=bio, 
            address_neighborhood=address_neighborhood,
            is_vip=False 
        )
        if category_ids:
            new_provider.categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
        
        db.add(new_provider)
        db.commit()

        return templates.TemplateResponse("cadastro.html", {
            "request": request, "categorias": categorias, "msg_sucesso": "Cadastro realizado com sucesso!"
        })
    except Exception as e:
        return templates.TemplateResponse("cadastro.html", {
            "request": request, "categorias": categorias, "msg_erro": f"Erro: {str(e)}"
        })

@app.get("/admin/virar-vip/{provider_id}")
def make_vip(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        provider.is_vip = True
        db.commit()
    return RedirectResponse(url="/")