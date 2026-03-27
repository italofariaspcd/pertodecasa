from fastapi import FastAPI, Depends, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from starlette.middleware.sessions import SessionMiddleware
import models, database, io, csv
from seed import LISTA_CIDADES_SE

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="caju_valley_master_2026")
templates = Jinja2Templates(directory="templates")

ADMIN_PASS = "Cica29xl!@"

@app.get("/healthcheck")
def healthcheck():
    return {"status": "online"}

@app.get("/")
def home(request: Request, q: str = None, db: Session = Depends(database.get_db)):
    destaques = db.query(models.Profissional).filter(models.Profissional.ativo == True, models.Profissional.is_destaque == True).limit(10).all()
    profissionais = []
    if q:
        q_l = f"%{q.strip()}%"
        profissionais = db.query(models.Profissional).join(models.Categoria).filter(
            models.Profissional.ativo == True,
            or_(models.Profissional.nome.ilike(q_l), models.Profissional.descricao.ilike(q_l), 
                models.Profissional.cidade.ilike(q_l), models.Categoria.nome.ilike(q_l))
        ).all()
    return templates.TemplateResponse("index.html", {"request": request, "profissionais": profissionais, "destaques": destaques, "termo": q, "msg": request.session.pop("msg", None)})

@app.get("/cadastrar")
def form_cad(request: Request, db: Session = Depends(database.get_db)):
    cats = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": cats, "cidades": sorted(LISTA_CIDADES_SE)})

@app.post("/processar-cadastro")
def salvar_anuncio(request: Request, nome: str = Form(...), telefone: str = Form(...), cidade: str = Form(...), endereco: str = Form(...), numero: str = Form(...), categoria_id: int = Form(...), descricao: str = Form(...), redes_sociais: str = Form(None), db: Session = Depends(database.get_db)):
    try:
        novo = models.Profissional(nome=nome, telefone=telefone, cidade=cidade, endereco=endereco, numero=numero, categoria_id=categoria_id, descricao=descricao, redes_sociais=redes_sociais)
        db.add(novo)
        db.commit()
        request.session["msg"] = "Enviado! Ativação via WhatsApp."
        return RedirectResponse(url="/", status_code=303)
    except:
        db.rollback()
        return RedirectResponse(url="/cadastrar", status_code=303)

@app.get("/login-admin")
def login_page(request: Request):
    return templates.TemplateResponse("login_admin.html", {"request": request})

@app.post("/admin-dashboard")
def admin_dash(request: Request, senha: str = Form(...), db: Session = Depends(database.get_db)):
    if senha != ADMIN_PASS: return templates.TemplateResponse("login_admin.html", {"request": request, "erro": True})
    profs = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profs})

@app.post("/admin/editar/{id}")
def editar_prof(id: int, nome: str = Form(...), telefone: str = Form(...), cidade: str = Form(...), endereco: str = Form(...), numero: str = Form(...), is_destaque: bool = Form(False), db: Session = Depends(database.get_db)):
    p = db.query(models.Profissional).get(id)
    if p:
        p.nome, p.telefone, p.cidade, p.endereco, p.numero, p.is_destaque = nome, telefone, cidade, endereco, numero, is_destaque
        db.commit()
    return RedirectResponse(url="/login-admin", status_code=303)

@app.get("/admin/exportar")
def exportar(db: Session = Depends(database.get_db)):
    profs = db.query(models.Profissional).all()
    out = io.StringIO()
    cw = csv.writer(out)
    cw.writerow(["Nome", "Tel", "Cidade", "Rua", "N", "Destaque"])
    for p in profs: cw.writerow([p.nome, p.telefone, p.cidade, p.endereco, p.numero, p.is_destaque])
    return Response(content=out.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=base_se.csv"})

@app.get("/admin/deletar/{id}")
def deletar(id: int, db: Session = Depends(database.get_db)):
    p = db.query(models.Profissional).get(id); db.delete(p); db.commit()
    return RedirectResponse(url="/login-admin", status_code=303)

@app.get("/contato")
def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})