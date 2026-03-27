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
app.add_middleware(SessionMiddleware, secret_key="caju-valley-v3-final-boss")
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = "Cica29xl!@"

@app.get("/")
def home(request: Request, q: Optional[str] = None, db: Session = Depends(get_db)):
    # Busca 6 profissionais aleatórios marcados como destaque
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

@app.post("/orcamento-coletivo")
def orcamento_coletivo(request: Request, cidade: str = Form(...), servico: str = Form(...)):
    # Redireciona para a busca combinada
    return RedirectResponse(url=f"/?q={servico} {cidade}", status_code=303)

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    # Importação dinâmica das cidades do seed para evitar repetição de código
    from seed import lista_cidades_se
    return templates.TemplateResponse("cadastro.html", {
        "request": request, "categorias": categorias, "cidades": sorted(lista_cidades_se)
    })

@app.post("/cadastrar")
def salvar_cadastro(request: Request, nome: str = Form(...), telefone: str = Form(...), redes_sociais: str = Form(None), endereco: str = Form(...), numero: str = Form(...), cidade: str = Form(...), descricao: str = Form(...), categoria_id: int = Form(...), db: Session = Depends(get_db)):
    novo = models.Profissional(nome=nome, telefone=telefone, redes_sociais=redes_sociais, endereco=endereco, numero=numero, cidade=cidade, descricao=descricao, categoria_id=categoria_id)
    db.add(novo)
    db.commit()
    request.session["mensagem_sucesso"] = "Cadastro enviado com sucesso! Aguarde ativação via WhatsApp."
    return RedirectResponse(url="/", status_code=303)

@app.get("/contato")
def pagina_contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@app.get("/login-admin")
def login_page(request: Request):
    return templates.TemplateResponse("login_admin.html", {"request": request})

@app.post("/admin")
def painel_admin(request: Request, senha: str = Form(...), db: Session = Depends(get_db)):
    if senha != ADMIN_PASSWORD:
        return templates.TemplateResponse("login_admin.html", {"request": request, "erro": "Senha incorreta!"})
    profissionais = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profissionais})

@app.get("/admin/deletar/{id}")
def deletar_profissional(id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).filter(models.Profissional.id == id).first()
    if prof:
        db.delete(prof)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)