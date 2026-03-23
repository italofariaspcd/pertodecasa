from database import engine, SessionLocal, Base
from models import Categoria

# Garante que as tabelas existem
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# MEGA LISTA DE CATEGORIAS DE SERVIÇOS
categorias = [
    # 🏠 Construção e Reformas
    {"name": "Pedreiro", "slug": "pedreiro"},
    {"name": "Eletricista", "slug": "eletricista"},
    {"name": "Encanador", "slug": "encanador"},
    {"name": "Pintor", "slug": "pintor"},
    {"name": "Marceneiro", "slug": "marceneiro"},
    {"name": "Gesseiro / Drywall", "slug": "gesseiro"},
    {"name": "Serralheiro", "slug": "serralheiro"},
    {"name": "Vidraceiro", "slug": "vidraceiro"},
    {"name": "Montador de Móveis", "slug": "montador-de-moveis"},
    {"name": "Instalador de Ar-condicionado", "slug": "instalador-ar-condicionado"},
    {"name": "Arquiteto(a)", "slug": "arquiteto"},
    {"name": "Engenheiro(a) Civil", "slug": "engenheiro-civil"},
    {"name": "Mestre de Obras", "slug": "mestre-de-obras"},
    {"name": "Impermeabilizador", "slug": "impermeabilizador"},
    {"name": "Tapeceiro", "slug": "tapeceiro"},
    {"name": "Limpeza de Terreno / Roçagem", "slug": "limpeza-terreno"},

    # 🧹 Serviços Domésticos
    {"name": "Diarista / Faxineira", "slug": "diarista-faxineira"},
    {"name": "Babá", "slug": "baba"},
    {"name": "Cuidador(a) de Idosos", "slug": "cuidador-idosos"},
    {"name": "Passadeira", "slug": "passadeira"},
    {"name": "Cozinheira", "slug": "cozinheira"},
    {"name": "Jardineiro", "slug": "jardineiro"},
    {"name": "Limpeza de Piscina", "slug": "limpeza-piscina"},
    {"name": "Desinsetização / Dedetização", "slug": "dedetizacao"},

    # 📱 Assistência Técnica
    {"name": "Manutenção de Celular", "slug": "manutencao-celular"},
    {"name": "Manutenção de Computador / TI", "slug": "manutencao-computador"},
    {"name": "Conserto de Geladeira / Freezer", "slug": "conserto-geladeira"},
    {"name": "Conserto de Máquina de Lavar", "slug": "conserto-maquina-lavar"},
    {"name": "Conserto de TV", "slug": "conserto-tv"},
    {"name": "Conserto de Micro-ondas", "slug": "conserto-microondas"},
    {"name": "Eletrodomésticos em Geral", "slug": "conserto-eletrodomesticos"},

    # 🚗 Automotivo
    {"name": "Mecânico", "slug": "mecanico"},
    {"name": "Socorro Automotivo / Guincho", "slug": "guincho"},
    {"name": "Eletricista de Autos", "slug": "eletricista-autos"},
    {"name": "Borracharia", "slug": "borracharia"},
    {"name": "Chaveiro", "slug": "chaveiro"},
    {"name": "Lavagem / Estética Automotiva", "slug": "estetica-automotiva"},

    # 💅 Beleza, Estética e Moda
    {"name": "Manicure e Pedicure", "slug": "manicure-pedicure"},
    {"name": "Cabeleireiro(a)", "slug": "cabeleireiro"},
    {"name": "Barbeiro", "slug": "barbeiro"},
    {"name": "Maquiador(a)", "slug": "maquiador"},
    {"name": "Designer de Sobrancelhas", "slug": "designer-sobrancelhas"},
    {"name": "Depiladora", "slug": "depiladora"},
    {"name": "Esteticista", "slug": "esteticista"},
    {"name": "Podólogo(a)", "slug": "podologo"},
    {"name": "Costureira / Alfaiate", "slug": "costureira"},
    {"name": "Sapateiro", "slug": "sapateiro"},

    # 🥳 Eventos e Gastronomia
    {"name": "Fotógrafo(a)", "slug": "fotografo"},
    {"name": "Videomaker / Filmagem", "slug": "videomaker"},
    {"name": "Confeiteira / Bolos", "slug": "confeiteira"},
    {"name": "Salgadeira", "slug": "salgadeira"},
    {"name": "Churrasqueiro", "slug": "churrasqueiro"},
    {"name": "Garçom / Barman", "slug": "garcom-barman"},
    {"name": "DJ", "slug": "dj"},
    {"name": "Músico / Cantor", "slug": "musico-cantor"},
    {"name": "Animador(a) de Festas", "slug": "animador-festas"},
    {"name": "Decoração de Eventos", "slug": "decoracao-eventos"},

    # 🚚 Transporte e Logística
    {"name": "Frete e Mudança", "slug": "frete-mudanca"},
    {"name": "Motoboy / Entregador", "slug": "motoboy"},
    {"name": "Motorista Particular / App", "slug": "motorista-particular"},
    {"name": "Transporte Escolar", "slug": "transporte-escolar"},

    # 📚 Aulas e Educação
    {"name": "Professor(a) Particular", "slug": "professor-particular"},
    {"name": "Aulas de Idiomas", "slug": "aulas-idiomas"},
    {"name": "Aulas de Música / Instrumentos", "slug": "aulas-musica"},
    {"name": "Reforço Escolar", "slug": "reforco-escolar"},

    # 🩺 Saúde e Bem-Estar
    {"name": "Personal Trainer", "slug": "personal-trainer"},
    {"name": "Massagista", "slug": "massagista"},
    {"name": "Nutricionista", "slug": "nutricionista"},
    {"name": "Psicólogo(a)", "slug": "psicologo"},
    {"name": "Fisioterapeuta", "slug": "fisioterapeuta"},
    {"name": "Enfermeiro(a)", "slug": "enfermeiro"},

    # 🐶 Pets
    {"name": "Banho e Tosa", "slug": "banho-tosa"},
    {"name": "Passeador de Cães (Dog Walker)", "slug": "passeador-caes"},
    {"name": "Adestrador", "slug": "adestrador"},
    {"name": "Veterinário(a)", "slug": "veterinario"},

    # 💼 Profissionais Liberais e Tech
    {"name": "Advogado(a)", "slug": "advogado"},
    {"name": "Contador(a)", "slug": "contador"},
    {"name": "Designer Gráfico", "slug": "designer-grafico"},
    {"name": "Programador / Desenvolvedor", "slug": "programador"},
    {"name": "Social Media / Marketing", "slug": "social-media"},
    {"name": "Consultor(a) Financeiro", "slug": "consultor-financeiro"}
]

print("Inserindo a MEGA lista de categorias no banco de dados...")
adicionadas = 0

for cat in categorias:
    # O script é inteligente: só adiciona se a categoria ainda não existir no banco
    existe = db.query(Categoria).filter_by(slug=cat["slug"]).first()
    if not existe:
        nova_cat = Categoria(name=cat["name"], slug=cat["slug"])
        db.add(nova_cat)
        adicionadas += 1

db.commit()
db.close()

if adicionadas > 0:
    print(f"✅ Sucesso! {adicionadas} novas categorias foram adicionadas.")
else:
    print("✅ O banco já possui todas essas categorias cadastradas.")