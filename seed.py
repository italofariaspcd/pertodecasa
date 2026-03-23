from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    
    # Lista massiva de categorias
    categorias_iniciais = [
        "Açougueiro", "Acupunturista", "Administrador(a)", "Advogado(a)", "Arquiteto(a)",
        "Artesão/Artesã", "Assistente Social", "Babá", "Banho e Tosa", "Barbeiro", 
        "Borracheiro", "Cabeleireiro(a)", "Carpinteiro", "Chaveiro", "Churrasqueiro", 
        "Confeiteira (Bolos e Doces)", "Conserto de Celulares", "Conserto de Eletrodomésticos", 
        "Contador(a)", "Corretor(a) de Imóveis", "Costureira", "Cozinheira", "Cuidador(a) de Idosos", 
        "Decorador de Festas", "Dentista", "Depiladora", "Designer Gráfico", "Designer de Interiores",
        "Designer de Sobrancelhas", "DJ / Som", "Diarista", "Eletricista", "Encanador", 
        "Engenheiro(a)", "Esteticista", "Estofador", "Faxineira", "Fisioterapeuta", 
        "Fonoaudiólogo(a)", "Fotógrafo(a)", "Fretes e Mudanças", "Garçom / Garçonete", 
        "Gesseiro", "Guias de Turismo", "Jardineiro", "Manicure e Pedicure", "Maquiador(a)", 
        "Marceneiro", "Massagista", "Mecânico de Autos", "Mecânico de Motos", 
        "Mestre de Obras", "Montador de Móveis", "Motoboy", "Motorista Particular", 
        "Nutricionista", "Passadeira", "Pedreiro", "Personal Trainer", "Pintor", 
        "Piscineiro", "Podólogo(a)", "Professor(a) Particular", "Psicólogo(a)", 
        "Salgadeira", "Segurança / Vigilante", "Serralheiro", "Soldador", "Tatuador(a)",
        "Técnico em Informática", "Técnico em Refrigeração", "Terapeuta", "Topógrafo",
        "Transporte Escolar", "Veterinário", "Videomaker", "Vidraceiro"
    ]
    
    # Ordena de A a Z
    categorias_iniciais.sort()
    # Adiciona "Outros" no final
    categorias_iniciais.append("Outros")
    
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