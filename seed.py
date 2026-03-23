from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    
    categorias_iniciais = [
        "Advogado(a)", "Babá", "Banho e Tosa", "Barbeiro", "Borracheiro", 
        "Cabeleireiro(a)", "Carpinteiro", "Chaveiro", "Churrasqueiro", 
        "Confeiteira (Bolos e Doces)", "Conserto de Celulares", 
        "Conserto de Eletrodomésticos", "Contador(a)", "Costureira", "Cozinheira", 
        "Cuidador(a) de Idosos", "Decorador de Festas", "Depiladora", 
        "Designer de Sobrancelhas", "DJ / Som", "Diarista", "Eletricista", 
        "Encanador", "Esteticista", "Faxineira", "Fisioterapeuta", "Fotógrafo", 
        "Fretes e Mudanças", "Garçom", "Gesseiro", "Jardineiro", "Manicure e Pedicure", 
        "Maquiador(a)", "Marceneiro", "Massagista", "Mecânico de Autos", 
        "Mecânico de Motos", "Mestre de Obras", "Montador de Móveis", "Motoboy", 
        "Motorista Particular", "Passadeira", "Pedreiro", "Personal Trainer", 
        "Pintor", "Piscineiro", "Professor(a) Particular", "Psicólogo(a)", 
        "Salgadeira", "Serralheiro", "Transporte Escolar", "Técnico em Informática", 
        "Técnico em Refrigeração", "Veterinário", "Videomaker", "Vidraceiro"
    ]
    
    # Ordena alfabeticamente antes de inserir
    categorias_iniciais.sort()
    
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