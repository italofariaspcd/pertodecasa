from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from starlette.middleware.sessions import SessionMiddleware
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="caju-valley-v3-dynamic")
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = "Cica29xl!@"

@app.get("/")
def home(request: Request, q: Optional[str] = None, db: Session = Depends(get_db)):
    # 1. Busca Profissionais em Destaque (is_destaque=True)
    destaque_list = db.query(models.Profissional).filter(
        models.Profissional.ativo == True,
        models.Profissional.is_destaque == True
    ).order_by(func.random()).limit(6).all()

    profissionais = []
    buscou = False
    sucesso = request.session.pop("mensagem_sucesso", None)

    if q and q.strip() != "":
        buscou = True
        profissionais = db.query(models.Profissional).filter(
            models.Profissional.ativo == True,
            or_(
                models.Profissional.nome.ilike(f"%{q}%"),
                models.Profissional.descricao.ilike(f"%{q}%"),
                models.Profissional.cidade.ilike(f"%{q}%")
            )
        ).all()
        
    return templates.TemplateResponse("index.html", {
        "request": request, "profissionais": profissionais, "destaques": destaque_list,
        "termo_busca": q, "buscou": buscou, "mensagem_sucesso": sucesso
    })

# 3. Rota para Orçamento Coletivo (Redireciona para busca específica)
@app.post("/orcamento-coletivo")
def orcamento_coletivo(request: Request, cidade: str = Form(...), servico: str = Form(...)):
    busca = f"{servico} {cidade}"
    return RedirectResponse(url=f"/?q={busca}", status_code=303)

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    # (Lista de cidades SE completa aqui...)
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": categorias})

@app.post("/cadastrar")
def salvar_cadastro(request: Request, nome: str = Form(...), telefone: str = Form(...), endereco: str = Form(...), numero: str = Form(...), cidade: str = Form(...), descricao: str = Form(...), categoria_id: int = Form(...), db: Session = Depends(get_db)):
    novo = models.Profissional(nome=nome, telefone=telefone, endereco=endereco, numero=numero, cidade=cidade, descricao=descricao, categoria_id=categoria_id)
    db.add(novo)
    db.commit()
    request.session["mensagem_sucesso"] = "Cadastro enviado! Aguarde contato via WhatsApp."
    return RedirectResponse(url="/", status_code=303)

@app.get("/login-admin")
def login_admin(request: Request):
    return templates.TemplateResponse("login_admin.html", {"request": request})

@app.post("/admin")
def painel_admin(request: Request, senha: str = Form(...), db: Session = Depends(get_db)):
    if senha != ADMIN_PASSWORD:
        return templates.TemplateResponse("login_admin.html", {"request": request, "erro": "Senha incorreta"})
    profissionais = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profissionais})