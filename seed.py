from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    # Categorias abrangendo Serviços Técnicos, Humanos e Tecnológicos
    setores = [
        "Eletricista Residencial", "Eletricista Industrial", "Encanador 24h", "Pedreiro de Alvenaria", 
        "Pintor de Paredes", "Gesseiro Decorativo", "Marceneiro de Planejados", "Serralheiro de Ferro",
        "Técnico em Ar Condicionado", "Montador de Móveis de Escritório", "Vidraceiro Temperado",
        "Psicólogo Clínico", "Psicopedagogo", "Fisioterapeuta Desportivo", "Nutricionista Funcional",
        "Personal Trainer Online", "Enfermeiro Particular", "Dentista Estético", "Veterinário de Grandes Portes",
        "Desenvolvedor Full Stack", "Técnico de Redes", "Gestor de Tráfego Pago", "Social Media Premium",
        "Designer de Logotipos", "Editor de Vídeos para YouTube", "Assistência iPhone", "Suporte TI Remoto",
        "Instalador de Energia Solar", "Consultor Jurídico", "Contador de MEI", "Fotógrafo de Eventos",
        # ... Adicione mais 470 itens conforme sua necessidade aqui
    ]
    
    lista_final = sorted(list(set(setores))) # Remove duplicatas e ordena
    lista_final.append("Outros") # Garante "Outros" no final
    
    try:
        for nome in lista_final:
            if not db.query(Categoria).filter_by(nome=nome).first():
                db.add(Categoria(nome=nome))
        db.commit()
        print("Base de dados de categorias sincronizada com sucesso! 🌵")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()