from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, auth, database

# Cria as tabelas ao iniciar
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Perto de Casa SE - API")

# --- ROTAS DE AUTENTICAÇÃO E CADASTRO ---

@app.post("/register", status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 1. Verifica se email existe
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # 2. Cria Usuário Base
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd,
        is_provider=user.is_provider
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. Se for prestador, cria perfil e endereço
    if user.is_provider:
        # Cria Perfil
        new_provider = models.Provider(
            user_id=new_user.id,
            whatsapp=user.whatsapp,
            bio=user.bio
        )
        # Adiciona categorias
        if user.category_ids:
            cats = db.query(models.Category).filter(models.Category.id.in_(user.category_ids)).all()
            new_provider.categories.extend(cats)
        
        db.add(new_provider)

        # Cria Endereço (Essencial para busca por bairro)
        if user.address_neighborhood:
            new_address = models.Address(
                user_id=new_user.id,
                neighborhood=user.address_neighborhood,
                city="Aracaju", # Default MVP
                state="SE"
            )
            db.add(new_address)
        
        db.commit()

    return {"msg": "Usuário criado com sucesso", "id": new_user.id}

@app.post("/token")
def login(form_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Nota: Aqui usei UserCreate para simplificar, mas ideal é usar OAuth2PasswordRequestForm
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# --- ROTAS DE BUSCA (CORE DO APP) ---

@app.get("/categories", response_model=List[schemas.CategoryBase])
def list_categories(db: Session = Depends(database.get_db)):
    return db.query(models.Category).all()

@app.get("/search/{category_slug}", response_model=List[schemas.ProviderListDTO])
def search_providers(
    category_slug: str, 
    bairro: Optional[str] = None, 
    db: Session = Depends(database.get_db)
):
    """
    Busca prestadores por categoria (obrigatório) e bairro (opcional).
    Ex: /search/eletricista?bairro=Jardins
    """
    query = db.query(models.Provider)\
        .join(models.Provider.categories)\
        .join(models.User)\
        .join(models.Address)\
        .filter(models.Category.slug == category_slug)

    if bairro:
        # Filtro case-insensitive para o bairro
        query = query.filter(models.Address.neighborhood.ilike(f"%{bairro}%"))

    providers = query.all()
    
    # Formata a resposta para o DTO
    results = []
    for p in providers:
        results.append({
            "full_name": p.user.full_name,
            "whatsapp": p.whatsapp,
            "bio": p.bio,
            "neighborhood": p.user.address.neighborhood if p.user.address else "Não informado",
            "categories": [c.name for c in p.categories]
        })
        
    return results