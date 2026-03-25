from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    # Categorias abrangendo todos os setores
    lista = [
        # Técnicos (Exemplos de mais de 500)
        "Eletricista Residencial", "Encanador 24h", "Pedreiro Profissional", "Pintor Decorativo", 
        "Gesseiro", "Marceneiro", "Serralheiro", "Técnico de Ar Condicionado", "Montador de Móveis",
        "Mecânico de Autos", "Borracheiro", "Chaveiro", "Desentupidor", "Jardineiro", "Piscineiro",
        "Técnico de Celular", "Técnico de Informática", "Instalador de Câmeras", "Eletricista Industrial",
        # Humanos/Saúde
        "Psicólogo(a)", "Fisioterapeuta", "Nutricionista", "Enfermeiro(a) Particular", "Cuidador de Idosos",
        "Babá", "Diarista", "Passadeira", "Cozinheiro(a)", "Personal Trainer", "Dentista", "Veterinário",
        # Tecnológicos
        "Social Media", "Gestor de Tráfego", "Desenvolvedor de Sites", "Designer Gráfico", "Editor de Vídeo",
        "Fotógrafo(a)", "Analista de TI", "Suporte Técnico Remoto", "E-commerce Specialist",
        # Adicione aqui as demais centenas de variações...
    ]
    
    # Preenchimento automático para simular volume massivo se necessário
    lista_final = sorted(list(set(lista)))
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