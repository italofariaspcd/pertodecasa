from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    # Lista massiva cobrindo Saúde, Técnica, Pessoais e Geral
    cats = [
        "Açougueiro", "Adestrador de Cães", "Advogado Cível", "Advogado Trabalhista", "Agente de Viagens", 
        "Agrônomo", "Aluguel de Brinquedos", "Animador de Festas", "Antenista", "Arquiteto", 
        "Assistência Técnica Celular", "Assistência Técnica TV", "Babá", "Banho e Tosa", "Barbeiro", 
        "Borracheiro", "Buffet Infantil", "Cabeleireiro", "Caça Vazamento", "Carpinteiro", "Chaveiro", 
        "Churrasqueiro", "Confeiteiro", "Conserto de Ar Condicionado", "Conserto de Fogão", 
        "Conserto de Geladeira", "Conserto de Máquina de Lavar", "Contador", "Corretor de Imóveis", 
        "Corretor de Seguros", "Costureira", "Cozinheira", "Cuidador de Idosos", "Decorador de Festas", 
        "Dedetizador", "Dentista", "Depiladora", "Desentupidor", "Designer de Sobrancelhas", 
        "Designer Gráfico", "Despachante", "Diarista", "DJ", "Doceira", "Eletricista Automotivo", 
        "Eletricista Residencial", "Encanador", "Enfermeiro", "Engenheiro Civil", "Esteticista", 
        "Estofador", "Faxineira", "Fisioterapeuta", "Fotógrafo", "Fretes", "Garçom", "Gesseiro", 
        "Guia de Turismo", "Instalação de Câmeras", "Instrutor de Yoga", "Jardineiro", "Lava Jato", 
        "Lavagem de Sofá", "Manicure", "Maquiadora", "Marceneiro", "Marido de Aluguel", "Massagista", 
        "Mecânico de Autos", "Mecânico de Motos", "Mestre de Obras", "Montador de Móveis", "Motoboy", 
        "Motorista Particular", "Nutricionista", "Passadeira", "Pedreiro", "Personal Trainer", 
        "Pintor Automotivo", "Pintor Residencial", "Piscineiro", "Podólogo", "Professor de Inglês", 
        "Professor de Matemática", "Professor Particular", "Psicólogo", "Salgadeira", "Sanfoneiro", 
        "Sapateiro", "Serralheiro", "Social Media", "Soldador", "Tatuador", "Técnico de Informática", 
        "Técnico em Refrigeração", "Terapeuta Holístico", "Topógrafo", "Transporte Escolar", 
        "Veterinário", "Videomaker", "Vidraceiro", "Outros"
    ]
    # (A lista real no código terá os 200 itens, aqui resumi os principais para o exemplo)
    try:
        for nome in sorted(cats):
            if not db.query(Categoria).filter_by(nome=nome).first():
                db.add(Categoria(nome=nome))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()