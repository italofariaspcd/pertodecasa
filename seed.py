from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    # Adicione aqui os 500+ itens categorizados por Técnicos, Humanos, Saúde e Tecnológicos
    setores = [
        # Técnicos
        "Eletricista", "Encanador", "Pedreiro", "Gesseiro", "Serralheiro", "Marceneiro", "Pintor",
        # Humanos
        "Psicólogo", "Advogado", "Professor Particular", "Babá", "Cuidador de Idosos",
        # Saúde
        "Fisioterapeuta", "Dentista", "Enfermeiro Particular", "Nutricionista",
        # Tecnológicos
        "Desenvolvedor de Sites", "Gestor de Tráfego", "Social Media", "Técnico de Celular",
        # ... Expanda esta lista até 500 itens
    ]
    
    lista_final = sorted(list(set(setores)))
    lista_final.append("Outros")
    
    try:
        for nome in lista_final:
            if not db.query(Categoria).filter_by(nome=nome).first():
                db.add(Categoria(nome=nome))
        db.commit()
        print("Mega lista sincronizada!")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()