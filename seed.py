from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    # Lista categorizada: Técnicos, Humanos, Saúde e Tecnológicos
    lista = [
        # TÉCNICOS/CONSTRUÇÃO
        "Eletricista Residencial", "Encanador", "Pedreiro", "Pintor", "Gesseiro", "Marceneiro", 
        "Serralheiro", "Mecânico de Autos", "Mecânico de Motos", "Técnico em Refrigeração", 
        "Montador de Móveis", "Vidraceiro", "Jardineiro", "Piscineiro", "Calheiro",
        # HUMANOS/SERVIÇOS
        "Cabeleireiro(a)", "Manicure/Pedicure", "Barbeiro", "Maquiador(a)", "Esteticista", 
        "Diarista", "Babá", "Cuidador de Idosos", "Cozinheiro(a)", "Confeiteiro(a)", 
        "Salgadeiro(a)", "Garçom/Garçonete", "Segurança Particular", "Motorista Particular",
        # SAÚDE
        "Fisioterapeuta", "Psicólogo(a)", "Nutricionista", "Personal Trainer", "Enfermeiro(a)", 
        "Dentista", "Fonoaudiólogo(a)", "Veterinário", "Terapeuta Holístico",
        # TECNOLÓGICOS/DIGITAIS
        "Desenvolvedor de Sites", "Técnico em Informática", "Social Media", "Designer Gráfico", 
        "Gestor de Tráfego", "Editor de Vídeo", "Assistência Técnica Celular", "Fotógrafo(a)",
        "E-commerce Specialist", "Suporte de TI", "Instalador de Câmeras/Alarmes"
    ]
    try:
        for nome in sorted(lista):
            if not db.query(Categoria).filter_by(nome=nome).first():
                db.add(Categoria(nome=nome))
        db.commit()
        print("Categorias atualizadas com sucesso! 🌵")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()