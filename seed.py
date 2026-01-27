from database import SessionLocal, engine, Base
from models import Category
from sqlalchemy.exc import IntegrityError

# Garante que as tabelas existam antes de inserir os dados
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Lista MÁXIMA de Categorias organizadas por "Grupos"
categorias_completas = [
    # --- MANUTENÇÃO E REPAROS ---
    {"name": "Ar-Condicionado e Refrigeração", "slug": "refrigeracao", "group": "Manutenção"},
    {"name": "Eletricista", "slug": "eletricista", "group": "Manutenção"},
    {"name": "Encanador / Bombeiro Hidráulico", "slug": "encanador", "group": "Manutenção"},
    {"name": "Pedreiro", "slug": "pedreiro", "group": "Construção"},
    {"name": "Pintor", "slug": "pintor", "group": "Construção"},
    {"name": "Marido de Aluguel", "slug": "marido-de-aluguel", "group": "Manutenção"},
    {"name": "Gesseiro", "slug": "gesseiro", "group": "Construção"},
    {"name": "Serralheiro", "slug": "serralheiro", "group": "Construção"},
    {"name": "Vidraceiro", "slug": "vidraceiro", "group": "Construção"},
    {"name": "Marceneiro", "slug": "marceneiro", "group": "Construção"},
    {"name": "Desentupidora", "slug": "desentupidora", "group": "Manutenção"},
    {"name": "Dedetizadora", "slug": "dedetizadora", "group": "Manutenção"},
    {"name": "Conserto de Telhados e Calhas", "slug": "telhados", "group": "Construção"},

    # --- TÉCNICA E ELETRÔNICOS ---
    {"name": "Assistência Técnica de Celular", "slug": "celular", "group": "Técnica"},
    {"name": "Formatação e PC", "slug": "informatica", "group": "Técnica"},
    {"name": "Conserto de Eletrodomésticos", "slug": "eletrodomesticos", "group": "Técnica"},
    {"name": "Instalação de Câmeras e Alarmes", "slug": "seguranca", "group": "Técnica"},
    {"name": "Instalação de Antenas e TV", "slug": "antenas", "group": "Técnica"},

    # --- BELEZA E BEM-ESTAR ---
    {"name": "Manicure e Pedicure", "slug": "manicure", "group": "Beleza"},
    {"name": "Cabeleireira", "slug": "cabeleireira", "group": "Beleza"},
    {"name": "Barbeiro", "slug": "barbeiro", "group": "Beleza"},
    {"name": "Design de Sobrancelhas", "slug": "sobrancelhas", "group": "Beleza"},
    {"name": "Depilação", "slug": "depilacao", "group": "Beleza"},
    {"name": "Maquiadora", "slug": "maquiadora", "group": "Beleza"},
    {"name": "Esteticista", "slug": "esteticista", "group": "Beleza"},
    {"name": "Massoterapeuta", "slug": "massagem", "group": "Bem-Estar"},
    {"name": "Podóloga", "slug": "podologia", "group": "Bem-Estar"},

    # --- SERVIÇOS DOMÉSTICOS ---
    {"name": "Diarista", "slug": "diarista", "group": "Doméstico"},
    {"name": "Passadeira", "slug": "passadeira", "group": "Doméstico"},
    {"name": "Lavadeira", "slug": "lavadeira", "group": "Doméstico"},
    {"name": "Limpeza de Estofados e Tapetes", "slug": "limpeza-estofados", "group": "Doméstico"},
    {"name": "Cozinheira em Domicílio", "slug": "cozinheira", "group": "Doméstico"},
    {"name": "Babá", "slug": "baba", "group": "Doméstico"},
    {"name": "Cuidador de Idosos", "slug": "cuidador", "group": "Doméstico"},
    {"name": "Jardineiro", "slug": "jardineiro", "group": "Doméstico"},
    {"name": "Piscineiro", "slug": "piscineiro", "group": "Doméstico"},

    # --- FESTAS E EVENTOS ---
    {"name": "Boleira / Confeiteira", "slug": "bolos", "group": "Festas"},
    {"name": "Salgadeiro(a)", "slug": "salgados", "group": "Festas"},
    {"name": "Churrasqueiro", "slug": "churrasqueiro", "group": "Festas"},
    {"name": "Decoração de Festas", "slug": "decoracao", "group": "Festas"},
    {"name": "Garçom e Copeira", "slug": "garcom", "group": "Festas"},
    {"name": "DJ e Som", "slug": "dj", "group": "Festas"},
    {"name": "Fotógrafo", "slug": "fotografo", "group": "Festas"},

    # --- SERVIÇOS DIVERSOS ---
    {"name": "Costureira e Ajustes", "slug": "costureira", "group": "Moda"},
    {"name": "Lavagem de Carro (Delivery)", "slug": "lava-jato", "group": "Automotivo"},
    {"name": "Mecânico", "slug": "mecanico", "group": "Automotivo"},
    {"name": "Borracheiro", "slug": "borracheiro", "group": "Automotivo"},
    {"name": "Fretes e Mudanças", "slug": "fretes", "group": "Transporte"},
    {"name": "Motoboy", "slug": "motoboy", "group": "Transporte"},
    {"name": "Passeador de Cães (Pet Sitter)", "slug": "pet-sitter", "group": "Pet"},
    {"name": "Banho e Tosa em Domicílio", "slug": "banho-tosa", "group": "Pet"},
    {"name": "Aulas Particulares / Reforço", "slug": "aulas", "group": "Educação"},
    {"name": "Personal Trainer", "slug": "personal", "group": "Saúde"},
]

print("Iniciando cadastro de categorias no banco de dados...")

count = 0
for cat_data in categorias_completas:
    # Verifica se já existe pelo 'slug' para não duplicar se você rodar o script 2 vezes
    exists = db.query(Category).filter_by(slug=cat_data["slug"]).first()
    
    if not exists:
        nova_cat = Category(
            name=cat_data["name"],
            slug=cat_data["slug"],
            group=cat_data["group"],
            icon="fa-circle" # Ícone padrão
        )
        db.add(nova_cat)
        count += 1

try:
    db.commit()
    print(f"Sucesso! {count} novas categorias foram cadastradas no 'Perto de Casa'.")
except Exception as e:
    db.rollback()
    print(f"Erro ao salvar: {e}")
finally:
    db.close()