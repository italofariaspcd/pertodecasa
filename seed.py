from database import SessionLocal, engine
from models import Base, Categoria

# Cria as tabelas
Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    categorias_iniciais = [
        "Eletricista", "Encanador", "Pedreiro", "Pintor", 
        "Diarista", "Manicure", "Cabeleireiro", "Mecânico",
        "Montador de Móveis", "Fretista", "Técnico em Informática",
        "Costureira", "Professor Particular", "Esteticista"
    ]
    
    print("Inserindo categorias no banco de dados...")
    try:
        for nome_cat in categorias_iniciais:
            existe = db.query(Categoria).filter_by(nome=nome_cat).first()
            if not existe:
                nova_cat = Categoria(nome=nome_cat)
                db.add(nova_cat)
        db.commit()
        print("Sucesso! Categorias prontas.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()