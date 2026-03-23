from database import SessionLocal, engine
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

def popular_categorias():
    db = SessionLocal()
    
    categorias = [
        "Açougueiro", "Acompanhante Terapêutico", "Acupunturista", "Adestrador de Cães", "Administrador(a)", 
        "Advogado(a)", "Agente de Viagens", "Aluguel de Equipamentos", "Animador de Festas", "Arquiteto(a)",
        "Artesão/Artesã", "Assistente Social", "Assistência Técnica TV", "Babá", "Banho e Tosa", 
        "Barbeiro", "Borracheiro", "Buffet Completo", "Cabeleireiro(a)", "Caçador de Vazamentos", 
        "Carpinteiro", "Carreto e Carretinha", "Chaveiro", "Churrasqueiro", "Coach", "Confeiteira (Bolos e Doces)", 
        "Conserto de Celulares", "Conserto de Eletrodomésticos", "Contador(a)", "Corretor(a) de Imóveis", 
        "Corretor de Seguros", "Costureira", "Cozinheira", "Cuidador(a) de Idosos", "Danceteria / Som", 
        "Decorador de Festas", "Dedetizador", "Dentista", "Depiladora", "Designer Gráfico", "Designer de Interiores",
        "Designer de Sobrancelhas", "Desentupidor", "Despachante", "Diarista", "DJ / Som", "Eletricista", 
        "Encanador", "Enfermeiro(a)", "Engenheiro(a)", "Esteticista", "Estofador", "Faxineira", "Fisioterapeuta", 
        "Fonoaudiólogo(a)", "Fotógrafo(a)", "Fretes e Mudanças", "Garçom / Garçonete", "Gesseiro", "Guia de Turismo", 
        "Instalador de Ar Condicionado", "Instalador de Câmeras", "Jardineiro", "Lava Jato", "Limpeza de Sofá", 
        "Manicure e Pedicure", "Maquiador(a)", "Marceneiro", "Marido de Aluguel", "Massagista", "Mecânico de Autos", 
        "Mecânico de Motos", "Mestre de Obras", "Montador de Móveis", "Motoboy", "Motorista Particular", 
        "Nutricionista", "Organizadora de Eventos", "Passadeira", "Pedreiro", "Personal Trainer", "Pintor", 
        "Piscineiro", "Podólogo(a)", "Professor(a) Particular", "Psicólogo(a)", "Salgadeira", "Segurança / Vigilante", 
        "Serralheiro", "Soldador", "Tatuador(a)", "Técnico em Informática", "Terapeuta", "Topógrafo",
        "Transporte Escolar", "Veterinário", "Videomaker", "Vidraceiro"
    ]
    
    categorias.sort()
    categorias.append("Outros")
    
    print("Semeando categorias...")
    try:
        for nome_cat in categorias:
            existe = db.query(Categoria).filter_by(nome=nome_cat).first()
            if not existe:
                db.add(Categoria(nome=nome_cat))
        db.commit()
        print("Categorias prontas!")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_categorias()