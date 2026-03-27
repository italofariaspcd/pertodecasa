from database import SessionLocal, engine
import models
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

LISTA_CIDADES_SE = [
    "Amparo de São Francisco", "Aquidabã", "Aracaju", "Arauá", "Areia Branca", "Barra dos Coqueiros", 
    "Boquim", "Brejo Grande", "Campo do Brito", "Canhoba", "Canindé de São Francisco", "Capela", 
    "Carira", "Carmópolis", "Cedro de São João", "Cristinápolis", "Cumbe", "Divina Pastora", 
    "Estância", "Feira Nova", "Frei Paulo", "Gararu", "General Maynard", "Gracho Cardoso", 
    "Ilha das Flores", "Indiaroba", "Itabaiana", "Itabaianinha", "Itaporanga d'Ajuda", "Japaratuba", 
    "Japoatã", "Lagarto", "Laranjeiras", "Macambira", "Malhada dos Bois", "Malhador", 
    "Maruim", "Moita Bonita", "Monte Alegre de Sergipe", "Muribeca", "Neópolis", "Nossa Senhora da Glória", 
    "Nossa Senhora das Dores", "Nossa Senhora de Lourdes", "Nossa Senhora do Socorro", "Pacatuba", 
    "Pedra Mole", "Pedrinhas", "Pinhão", "Pirambu", "Poço Redondo", "Poço Verde", "Porto da Folha", 
    "Propriá", "Riachão do Dantas", "Riachuelo", "Ribeirópolis", "Rosário do Catete", "Salgado", 
    "Santa Luzia do Itanhy", "Santa Rosa de Lima", "Santana do São Francisco", "Santo Amaro das Brotas", 
    "São Cristóvão", "São Domingos", "São Francisco", "São Miguel do Aleixo", "Simão Dias", 
    "Siriri", "Telha", "Tobias Barreto", "Tomar do Geru", "Umbaúba"
]

# Exemplo de expansão para as 1000 categorias (Adicione as suas aqui)
CATEGORIAS_MASTER = [
    "Açougueiro", "Adestrador", "Advogado Cível", "Advogado Trabalhista", "Agente de Viagens",
    "Arquiteto", "Assistência Celular", "Babá", "Barbeiro", "Borracheiro", "Cabeleireiro",
    "Caminhão Pipa", "Chaveiro", "Confeiteiro", "Contador", "Costureira", "Cozinheiro",
    "Diarista", "Eletricista", "Encanador", "Engenheiro", "Estofador", "Fisioterapeuta",
    "Fotógrafo", "Frete", "Gesseiro", "Jardineiro", "Lava Jato", "Manicure", "Marceneiro",
    "Mecânico", "Montador de Móveis", "Motoboy", "Nutricionista", "Pedreiro", "Pintor",
    "Psicólogo", "Serralheiro", "Técnico de TI", "Vidraceiro", "Outros"
]

def popular_sistema():
    db = SessionLocal()
    print("🚀 Sincronizando Sergipe e Categorias... 🌵")
    lista_final = sorted(list(set(CATEGORIAS_MASTER)))
    if "Outros" in lista_final: lista_final.remove("Outros")
    lista_final.append("Outros")

    for nome in lista_final:
        if not db.query(Categoria).filter_by(nome=nome).first():
            db.add(Categoria(nome=nome))
    db.commit()
    db.close()
    print("✅ Banco pronto!")

if __name__ == "__main__":
    popular_sistema()