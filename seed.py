from database import SessionLocal, engine
import models
from models import Base, Categoria

Base.metadata.create_all(bind=engine)

LISTA_CIDADES_SE = ["Amparo de São Francisco", "Aquidabã", "Aracaju", "Arauá", "Areia Branca", "Barra dos Coqueiros", "Boquim", "Brejo Grande", "Campo do Brito", "Canhoba", "Canindé de São Francisco", "Capela", "Carira", "Carmópolis", "Cedro de São João", "Cristinápolis", "Cumbe", "Divina Pastora", "Estância", "Feira Nova", "Frei Paulo", "Gararu", "General Maynard", "Gracho Cardoso", "Ilha das Flores", "Indiaroba", "Itabaiana", "Itabaianinha", "Itaporanga d'Ajuda", "Japaratuba", "Japoatã", "Lagarto", "Laranjeiras", "Macambira", "Malhada dos Bois", "Malhador", "Maruim", "Moita Bonita", "Monte Alegre de Sergipe", "Muribeca", "Neópolis", "Nossa Senhora da Glória", "Nossa Senhora das Dores", "Nossa Senhora de Lourdes", "Nossa Senhora do Socorro", "Pacatuba", "Pedra Mole", "Pedrinhas", "Pinhão", "Pirambu", "Poço Redondo", "Poço Verde", "Porto da Folha", "Propriá", "Riachão do Dantas", "Riachuelo", "Ribeirópolis", "Rosário do Catete", "Salgado", "Santa Luzia do Itanhy", "Santa Rosa de Lima", "Santana do São Francisco", "Santo Amaro das Brotas", "São Cristóvão", "São Domingos", "São Francisco", "São Miguel do Aleixo", "Simão Dias", "Siriri", "Telha", "Tobias Barreto", "Tomar do Geru", "Umbaúba"]

CATEGORIAS_100 = ["Açougueiro", "Adestrador", "Advogado Cível", "Advogado Trabalhista", "Agente de Viagens", "Agrônomo", "Aluguel de Brinquedos", "Analista de TI", "Animador de Festas", "Arquiteto", "Artesão", "Assistência Celular", "Assistência TV", "Astrólogo", "Babá", "Barbeiro", "Bartender", "Borracheiro", "Buffet", "Cabeleireiro", "Caminhão Pipa", "Carpinteiro", "Chaveiro", "Coach", "Confeiteiro", "Contador", "Costureira", "Cozinheiro", "Cuidador de Idosos", "Decorador", "Dentista", "Depiladora", "Designer Gráfico", "Diarista", "DJ", "Doula", "Eletricista", "Encanador", "Enfermeiro", "Engenheiro Civil", "Estofador", "Esteticista", "Fisioterapeuta", "Fotógrafo", "Frete e Mudança", "Gesseiro", "Guia de Turismo", "Instalador de Ar", "Jardineiro", "Lava Jato", "Limpeza de Fossa", "Limpeza de Piscina", "Manicure", "Maquiador", "Marceneiro", "Marido de Aluguel", "Massagista", "Mecânico de Autos", "Mecânico de Motos", "Montador de Móveis", "Motoboy", "Motorista Particular", "Nutricionista", "Organizador de Eventos", "Padeiro", "Paisagista", "Pedreiro", "Personal Trainer", "Pintor", "Podólogo", "Porteiro", "Professor Particular", "Psicólogo", "Salgadeiro", "Sapateiro", "Serralheiro", "Social Media", "Tatuador", "Técnico de Informática", "Terapeuta", "Tradutor", "Transporte Escolar", "Vendedor", "Veterinário", "Vidraceiro", "Yoga", "Outros"]

def popular_sistema():
    db = SessionLocal()
    print("🚀 Sincronizando Sergipe e Categorias Master... 🌵")
    lista_cats = sorted(list(set(CATEGORIAS_100)))
    if "Outros" in lista_cats: lista_cats.remove("Outros")
    lista_cats.append("Outros")

    for nome in lista_cats:
        if not db.query(Categoria).filter_by(nome=nome).first():
            db.add(Categoria(nome=nome))
    db.commit()
    db.close()
    print("✅ Banco pronto para o Deploy!")

if __name__ == "__main__":
    popular_sistema()