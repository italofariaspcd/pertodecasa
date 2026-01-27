from database import SessionLocal, engine
from models import Base, Category
import unicodedata
import re

# 1. Garante que as tabelas existem
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 2. Lista GIGANTE de Categorias
categorias = [
    # --- NOVOS PEDIDOS ---
    "Vendedor de Doces",
    "Cuidador de Pets",
    "Nômade Digital",
    "Manutenção de Computadores",
    "Consultor",
    "Organizador de Festa",
    "Escritor de Convites",
    
    # --- COACHING PESSOAL ---
    "Coaching Pessoal",
    "Coach de Relacionamentos",
    "Coach de Inteligência Emocional",
    "Coach Financeiro",
    "Coach Espiritual",
    "Coach de Emagrecimento",
    "Coach Esportivo",

    # --- COACHING PROFISSIONAL ---
    "Coaching Profissional",
    "Coach Corporativo",
    "Coach de Performance",
    "Coach de Carreira",
    "Coach de Equipes",
    "Coach de Liderança",
    "Coach de Vendas",

    # --- SERVIÇOS ESSENCIAIS (Mantidos) ---
    "Pedreiro",
    "Pintor",
    "Eletricista",
    "Encanador",
    "Gesseiro",
    "Marceneiro",
    "Serralheiro",
    "Vidraceiro",
    "Mestre de Obras",
    
    # --- DOMÉSTICO ---
    "Faxina",
    "Diarista",
    "Passadeira",
    "Cozinheira",
    "Jardineiro",
    "Piscineiro",
    "Babá",
    "Cuidador de Idosos",

    # --- BELEZA ---
    "Cabeleireiro",
    "Barbeiro",
    "Manicure / Pedicure",
    "Maquiadora",
    "Designer de Sobrancelhas",
    "Depiladora",

    # --- ALIMENTAÇÃO ---
    "Boleira",
    "Salgadeira",
    "Confeiteira",
    "Churrasqueiro",
    "Garçom",

    # --- TÉCNICA E TRANSPORTE ---
    "Técnico de Celular",
    "Técnico de Ar-condicionado",
    "Técnico de Geladeira",
    "Montador de Móveis",
    "Motorista / Frete",
    "Motoboy",
    
    # --- ENSINO ---
    "Professor Particular",
    "Personal Trainer"
]

# Função auxiliar para criar slugs limpos (remove acentos e caracteres especiais)
def criar_slug(texto):
    # Normaliza para ASCII (remove acentos)
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.lower().strip()
    # Remove caracteres que não sejam letras, números ou espaços
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    # Troca espaços por traços
    texto = re.sub(r'[\s]+', '-', texto)
    return texto

print("🌱 Plantando categorias no Perto de Casa Nordeste...")

count = 0
for nome in categorias:
    slug = criar_slug(nome)
    
    # Verifica se já existe
    existe = db.query(Category).filter(Category.slug == slug).first()
    if not existe:
        nova_cat = Category(name=nome, slug=slug)
        db.add(nova_cat)
        print(f"✅ {nome} adicionado!")
        count += 1
    else:
        # Se já existe, ignoramos (para não dar erro)
        pass

db.commit()
db.close()

if count == 0:
    print("\n⚠️ Nenhuma categoria nova precisou ser adicionada (todas já existiam).")
else:
    print(f"\n🎉 Sucesso! {count} novas categorias adicionadas ao sistema.")