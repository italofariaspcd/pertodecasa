from fastapi import FastAPI, Depends, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from starlette.middleware.sessions import SessionMiddleware
import models, database, io, csv
from seed import LISTA_CIDADES_SE

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="caju-valley-master-key-2026")
templates = Jinja2Templates(directory="templates")

ADMIN_PASS = "Cica29xl!@"

@app.get("/healthcheck")
def healthcheck():
    return {"status": "online", "message": "Perto de Casa SE Ativo"}

@app.get("/")
def home(request: Request, q: str = None, db: Session = Depends(database.get_db)):
    destaques = db.query(models.Profissional).filter(models.Profissional.ativo == True, models.Profissional.is_destaque == True).order_by(func.random()).limit(6).all()
    profissionais = []
    if q:
        q_l = q.strip()
        profissionais = db.query(models.Profissional).join(models.Categoria).filter(
            models.Profissional.ativo == True,
            or_(
                models.Profissional.nome.ilike(f"%{q_l}%"),
                models.Profissional.descricao.ilike(f"%{q_l}%"),
                models.Profissional.cidade.ilike(f"%{q_l}%"),
                models.Categoria.nome.ilike(f"%{q_l}%")
            )
        ).all()
    return templates.TemplateResponse("index.html", {"request": request, "profissionais": profissionais, "destaques": destaques, "termo_busca": q, "msg": request.session.pop("msg", None)})

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(database.get_db)):
    cats = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {"request": request, "categorias": cats, "cidades": sorted(LISTA_CIDADES_SE)})

@app.post("/cadastrar-anuncio")
def salvar_anuncio(request: Request, nome: str = Form(...), telefone: str = Form(...), cidade: str = Form(...), endereco: str = Form(...), numero: str = Form(...), categoria_id: int = Form(...), descricao: str = Form(...), redes_sociais: str = Form(None), db: Session = Depends(database.get_db)):
    try:
        novo = models.Profissional(nome=nome, telefone=telefone, cidade=cidade, endereco=endereco, numero=numero, categoria_id=categoria_id, descricao=descricao, redes_sociais=redes_sociais)
        db.add(novo)
        db.commit()
        request.session["msg"] = "Cadastro enviado! Ativação via WhatsApp."
        return RedirectResponse(url="/", status_code=303)
    except Exception:
        db.rollback()
        return RedirectResponse(url="/cadastro", status_code=303)

@app.get("/login-admin")
def login_admin(request: Request):
    return templates.TemplateResponse("login_admin.html", {"request": request})

@app.post("/painel-admin")
def painel_admin(request: Request, senha: str = Form(...), db: Session = Depends(database.get_db)):
    if senha != ADMIN_PASS:
        return templates.TemplateResponse("login_admin.html", {"request": request, "erro": "Senha Incorreta!"})
    profs = db.query(models.Profissional).all()
    cats = db.query(models.Categoria).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profs, "categorias": cats, "cidades": sorted(LISTA_CIDADES_SE)})

@app.post("/admin/editar/{id}")
def editar_admin(id: int, nome: str = Form(...), telefone: str = Form(...), cidade: str = Form(...), is_destaque: bool = Form(False), db: Session = Depends(database.get_db)):
    prof = db.query(models.Profissional).get(id)
    if prof:
        prof.nome = nome
        prof.telefone = telefone
        prof.cidade = cidade
        prof.is_destaque = is_destaque
        db.commit()
    return RedirectResponse(url="/login-admin", status_code=303)

@app.get("/admin/exportar")
def exportar_dados(db: Session = Depends(database.get_db)):
    profs = db.query(models.Profissional).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nome", "Telefone", "Cidade", "Categoria"])
    for p in profs:
        writer.writerow([p.id, p.nome, p.telefone, p.cidade, p.categoria.nome])
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=banco_pertodecasa.csv"})

@app.get("/admin/deletar/{id}")
def deletar(id: int, db: Session = Depends(database.get_db)):
    prof = db.query(models.Profissional).get(id)
    if prof: db.delete(prof); db.commit()
    return RedirectResponse(url="/login-admin", status_code=303)

@app.get("/contato")
def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@app.post("/orcamento-coletivo")
def orcamento(cidade: str = Form(...), servico: str = Form(...)):
    return RedirectResponse(url=f"/?q={servico} {cidade}", status_code=303)