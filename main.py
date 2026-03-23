from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request, q: Optional[str] = None, db: Session = Depends(get_db)):
    profissionais = []
    buscou = False
    
    if q and q.strip() != "":
        buscou = True
        query = db.query(models.Profissional).filter(models.Profissional.ativo == True)
        query = query.filter(or_(
            models.Profissional.nome.ilike(f"%{q}%"),
            models.Profissional.descricao.ilike(f"%{q}%"),
            models.Profissional.cidade.ilike(f"%{q}%")
        ))
        profissionais = query.all()
        
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "profissionais": profissionais, 
        "termo_busca": q,
        "buscou": buscou
    })

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": categorias})

@app.post("/cadastrar")
def salvar_cadastro(
    nome: str = Form(...), telefone: str = Form(...), cidade: str = Form(...),
    descricao: str = Form(...), categoria_id: int = Form(...),
    taxaMensal: bool = Form(...), redes_sociais: Optional[str] = Form(""),
    db: Session = Depends(get_db)
):
    db.add(models.Profissional(
        nome=nome, telefone=telefone, cidade=cidade, descricao=descricao,
        categoria_id=categoria_id, redes_sociais=redes_sociais,
        aceitou_taxa=taxaMensal, ativo=True 
    ))
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/contato")
def pagina_contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

# --- ADMIN ---
@app.get("/admin")
def painel_admin(request: Request, db: Session = Depends(get_db)):
    profissionais = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profissionais})

@app.get("/admin/alternar/{prof_id}")
def alternar_status(prof_id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).get(prof_id)
    if prof:
        prof.ativo = not prof.ativo
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/deletar/{prof_id}")
def deletar_profissional(prof_id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).get(prof_id)
    if prof:
        db.delete(prof)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/editar/{prof_id}")
def form_editar(prof_id: int, request: Request, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).get(prof_id)
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("editar.html", {"request": request, "profissional": prof, "categorias": categorias})

@app.post("/admin/editar/{prof_id}")
def salvar_edicao(
    prof_id: int, nome: str = Form(...), telefone: str = Form(...),
    cidade: str = Form(...), descricao: str = Form(...),
    categoria_id: int = Form(...), redes_sociais: Optional[str] = Form(""),
    db: Session = Depends(get_db)
):
    prof = db.query(models.Profissional).get(prof_id)
    if prof:
        prof.nome, prof.telefone, prof.cidade = nome, telefone, cidade
        prof.descricao, prof.categoria_id, prof.redes_sociais = descricao, categoria_id, redes_sociais
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)