from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from starlette.middleware.sessions import SessionMiddleware
import models, database
from seed import LISTA_CIDADES_SE

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="caju-valley-v3-final")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request, q: str = None, db: Session = Depends(database.get_db)):
    destaques = db.query(models.Profissional).filter(models.Profissional.ativo == True, models.Profissional.is_destaque == True).order_by(func.random()).limit(6).all()
    profissionais = []
    if q:
        profissionais = db.query(models.Profissional).filter(models.Profissional.ativo == True, or_(models.Profissional.nome.ilike(f"%{q}%"), models.Profissional.descricao.ilike(f"%{q}%"), models.Profissional.cidade.ilike(f"%{q}%"))).all()
    return templates.TemplateResponse("index.html", {"request": request, "profissionais": profissionais, "destaques": destaques, "termo_busca": q, "msg": request.session.pop("msg", None)})

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(database.get_db)):
    cats = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": cats, "cidades": sorted(LISTA_CIDADES_SE)})

@app.post("/cadastrar")
def salvar(request: Request, nome: str = Form(...), telefone: str = Form(...), redes_sociais: str = Form(None), endereco: str = Form(...), numero: str = Form(...), cidade: str = Form(...), categoria_id: int = Form(...), descricao: str = Form(...), db: Session = Depends(database.get_db)):
    try:
        novo = models.Profissional(
            nome=nome, telefone=telefone, redes_sociais=redes_sociais,
            endereco=endereco, numero=numero, cidade=cidade,
            categoria_id=categoria_id, descricao=descricao
        )
        db.add(novo)
        db.commit()
        request.session["msg"] = "Cadastro enviado com sucesso! Aguarde ativação."
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Erro: {e}")
        return RedirectResponse(url="/cadastro", status_code=303)

@app.get("/contato")
def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@app.post("/orcamento-coletivo")
def orcamento(cidade: str = Form(...), servico: str = Form(...)):
    return RedirectResponse(url=f"/?q={servico} {cidade}", status_code=303)