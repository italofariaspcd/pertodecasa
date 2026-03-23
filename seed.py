from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    
    categorias_iniciais = [
        "Pedreiro", "Eletricista", "Encanador", "Pintor", "Carpinteiro", 
        "Marceneiro", "Serralheiro", "Gesseiro", "Vidraceiro", "Mestre de Obras",
        "Diarista", "Faxineira", "Babá", "Cuidador(a) de Idosos", 
        "Cozinheira", "Jardineiro", "Piscineiro", "Passadeira",
        "Técnico em Refrigeração", "Técnico em Informática", 
        "Conserto de Celulares", "Conserto de Eletrodomésticos", "Montador de Móveis", 
        "Chaveiro", "Mecânico de Autos", "Mecânico de Motos", "Borracheiro",
        "Manicure e Pedicure", "Cabeleireiro(a)", "Barbeiro", "Maquiador(a)", 
        "Esteticista", "Designer de Sobrancelhas", "Depiladora", "Massagista",
        "Confeiteira (Bolos e Doces)", "Salgadeira", "Churrasqueiro", "Garçom", 
        "Fotógrafo", "Videomaker", "Decorador de Festas", "DJ / Som",
        "Fretes e Mudanças", "Motoboy", "Motorista Particular", "Transporte Escolar",
        "Professor(a) Particular", "Personal Trainer", "Advogado(a)", 
        "Contador(a)", "Fisioterapeuta", "Psicólogo(a)", "Veterinário", "Banho e Tosa"
    ]
    
    print("Inserindo categorias...")
    try:
        for nome_cat in categorias_iniciais:
            existe = db.query(Categoria).filter_by(nome=nome_cat).first()
            if not existe:
                nova_cat = Categoria(nome=nome_cat)
                db.add(nova_cat)
        db.commit()
        print("Categorias criadas com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()