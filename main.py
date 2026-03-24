from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.middleware.sessions import SessionMiddleware
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="caju-valley-nordeste-2026")
templates = Jinja2Templates(directory="templates")

CIDADES_SE = [
    "Amparo de São Francisco", "Aquidabã", "Aracaju", "Arauá", "Areia Branca", "Barra dos Coqueiros", 
    "Boquim", "Brejo Grande", "Campo do Brito", "Canhoba", "Canindé de São Francisco", "Capela", 
    "Carira", "Carmópolis", "Cedro de São João", "Cristinápolis", "Cumbe", "Divina Pastora", 
    "Estância", "Feira Nova", "Frei Paulo", "Gararu", "General Maynard", "Gracho Cardoso", 
    "Ilha das Flores", "Indiaroba", "Itabaiana", "Itabaianinha", "Itaporanga d'Ajuda", "Japaratuba", 
    "Japoatã", "Lagarto", "Laranjeiras", "Macambira", "Malhada dos Bois", "Malhador", 
    "Maruim", "Moita Bonita", "Monte Alegre de Sergipe", "Muribeca", "Neópolis", "Nossa Senhora da Glória", 
    "Nossa Senhora das Dores", "Nossa Senhora de Lourdes", "Nossa Senhora do Socorro", "Pacatuba", 
    "Pedra Mole", "Pedrinhas", "Pinhão", "Pirambu", "Poço Redondo", "Poço Verde", "Porto da Folha", 
    "Propriá", "Riachão do Dantas", "Riachuelo", "Ribeirópolis", "Rosário do Catete", "Salgado", 
    "Santa Luzia do Itanhy", "Santa Rosa de Lima", "Santana do São Francisco", "Santo Amaro das Brotas", 
    "São Cristóvão", "São Domingos", "São Francisco", "São Miguel do Aleixo", "Simão Dias", 
    "Siriri", "Telha", "Tobias Barreto", "Tomar do Geru", "Umbaúba"
]

@app.get("/")
def home(request: Request, q: str = None, db: Session = Depends(get_db)):
    profissionais = []
    sucesso = request.session.pop("mensagem_sucesso", None)
    if q:
        profissionais = db.query(models.Profissional).filter(
            models.Profissional.ativo == True,
            or_(
                models.Profissional.nome.ilike(f"%{q}%"), 
                models.Profissional.descricao.ilike(f"%{q}%"), 
                models.Profissional.cidade.ilike(f"%{q}%")
            )
        ).all()
    return templates.TemplateResponse("index.html", {
        "request": request, "profissionais": profissionais, "termo_busca": q, "mensagem_sucesso": sucesso
    })

@app.get("/cadastro")
def form_cadastro(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("cadastro.html", {
        "request": request, "categorias": categorias, "cidades": sorted(CIDADES_SE)
    })

@app.post("/cadastrar")
def salvar_cadastro(
    request: Request, 
    nome: str = Form(...), 
    telefone: str = Form(...), 
    redes_sociais: str = Form(None), 
    endereco: str = Form(...), 
    numero: str = Form(...), 
    cidade: str = Form(...), 
    descricao: str = Form(...), 
    categoria_id: int = Form(...), 
    db: Session = Depends(get_db)
):
    db.add(models.Profissional(
        nome=nome, telefone=telefone, redes_sociais=redes_sociais, 
        endereco=endereco, numero=numero, cidade=cidade, 
        descricao=descricao, categoria_id=categoria_id
    ))
    db.commit()
    request.session["mensagem_sucesso"] = "Cadastro realizado com sucesso!"
    return RedirectResponse(url="/", status_code=303)

@app.get("/admin")
def admin(request: Request, db: Session = Depends(get_db)):
    profs = db.query(models.Profissional).all()
    return templates.TemplateResponse("admin.html", {"request": request, "profissionais": profs})

@app.get("/admin/editar/{prof_id}")
def form_editar(prof_id: int, request: Request, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).filter(models.Profissional.id == prof_id).first()
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    return templates.TemplateResponse("editar.html", {
        "request": request, "profissional": prof, "categorias": categorias, "cidades": sorted(CIDADES_SE)
    })

@app.post("/admin/editar/{prof_id}")
def salvar_edicao(
    prof_id: int, 
    nome: str = Form(...), 
    telefone: str = Form(...), 
    cidade: str = Form(...), 
    endereco: str = Form(...), 
    numero: str = Form(...), 
    descricao: str = Form(...), 
    categoria_id: int = Form(...), 
    redes_sociais: str = Form(None),
    db: Session = Depends(get_db)
):
    prof = db.query(models.Profissional).filter(models.Profissional.id == prof_id).first()
    if prof:
        prof.nome, prof.telefone, prof.cidade, prof.endereco, prof.numero = nome, telefone, cidade, endereco, numero
        prof.descricao, prof.categoria_id, prof.redes_sociais = descricao, categoria_id, redes_sociais
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/deletar/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Profissional).get(id)
    if prof:
        db.delete(prof)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/contato")
def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})