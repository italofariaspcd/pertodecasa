from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    # FILTRO NOVO: Só exibe quem está com ativo=True
    profissionais = db.query(models.Profissional).filter(models.Profissional.ativo == True).all()
    return templates.TemplateResponse("index.html", {"request": request, "profissionais": profissionais})

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": categorias})

@app.post("/cadastrar")
def salvar_cadastro(
    nome: str = Form(...),
    telefone: str = Form(...),
    cidade: str = Form(...),
    descricao: str = Form(...),
    categoria_id: int = Form(...),
    taxaMensal: bool = Form(...), # NOVO: Recebe o aceite da taxa
    db: Session = Depends(get_db)
):
    novo_profissional = models.Profissional(
        nome=nome,
        telefone=telefone,
        cidade=cidade,
        descricao=descricao,
        categoria_id=categoria_id,
        aceitou_taxa=taxaMensal, # NOVO: Salva que ele aceitou
        ativo=True               # NOVO: Já entra ativo no site
    )
    db.add(novo_profissional)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
# ==========================================
# ÁREA DO ADMINISTRADOR
# ==========================================

@app.get("/admin")
def painel_admin(request: Request, db: Session = Depends(get_db)):
    # Puxa TODOS os profissionais (ativos e inativos)
    profissionais = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profissionais})

@app.get("/admin/alternar/{prof_id}")
def alternar_status(prof_id: int, db: Session = Depends(get_db)):
    # Muda o status de Ativo para Inativo, e vice-versa
    prof = db.query(models.Profissional).filter(models.Profissional.id == prof_id).first()
    if prof:
        prof.ativo = not prof.ativo
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/deletar/{prof_id}")
def deletar_profissional(prof_id: int, db: Session = Depends(get_db)):
    # Apaga o profissional do banco de dados definitivamente
    prof = db.query(models.Profissional).filter(models.Profissional.id == prof_id).first()
    if prof:
        db.delete(prof)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)