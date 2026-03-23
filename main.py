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