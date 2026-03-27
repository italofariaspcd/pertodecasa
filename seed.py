from database import SessionLocal, engine
import models

LISTA_CIDADES_SE = ["Amparo de São Francisco", "Aquidabã", "Aracaju", "Arauá", "Areia Branca", "Barra dos Coqueiros", "Boquim", "Brejo Grande", "Campo do Brito", "Canhoba", "Canindé de São Francisco", "Capela", "Carira", "Carmópolis", "Cedro de São João", "Cristinápolis", "Cumbe", "Divina Pastora", "Estância", "Feira Nova", "Frei Paulo", "Gararu", "General Maynard", "Gracho Cardoso", "Ilha das Flores", "Indiaroba", "Itabaiana", "Itabaianinha", "Itaporanga d'Ajuda", "Japaratuba", "Japoatã", "Lagarto", "Laranjeiras", "Macambira", "Malhada dos Bois", "Malhador", "Maruim", "Moita Bonita", "Monte Alegre de Sergipe", "Muribeca", "Neópolis", "Nossa Senhora da Glória", "Nossa Senhora das Dores", "Nossa Senhora de Lourdes", "Nossa Senhora do Socorro", "Pacatuba", "Pedra Mole", "Pedrinhas", "Pinhão", "Pirambu", "Poço Redondo", "Poço Verde", "Porto da Folha", "Propriá", "Riachão do Dantas", "Riachuelo", "Ribeirópolis", "Rosário do Catete", "Salgado", "Santa Luzia do Itanhy", "Santa Rosa de Lima", "Santana do São Francisco", "Santo Amaro das Brotas", "São Cristóvão", "São Domingos", "São Francisco", "São Miguel do Aleixo", "Simão Dias", "Siriri", "Telha", "Tobias Barreto", "Tomar do Geru", "Umbaúba"]

def popular_sistema():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    categorias = ["Açougueiro", "Adestrador", "Advogado", "Agente de Viagens", "Arquiteto", "Assistência Celular", "Assistência TV", "Babá", "Barbeiro", "Borracheiro", "Cabeleireiro", "Caminhão Pipa", "Carpinteiro", "Chaveiro", "Confeiteiro", "Contador", "Costureira", "Cozinheiro", "Cuidador de Idosos", "Dentista", "Diarista", "DJ", "Doceria", "Eletricista", "Encanador", "Enfermeiro", "Engenheiro Civil", "Estofador", "Fisioterapeuta", "Fotógrafo", "Frete", "Gesseiro", "Jardineiro", "Lava Jato", "Limpeza de Piscina", "Manicure", "Maquiador", "Marceneiro", "Marido de Aluguel", "Mecânico", "Montador de Móveis", "Motoboy", "Nutricionista", "Pedreiro", "Personal Trainer", "Pintor", "Psicólogo", "Serralheiro", "Técnico de TI", "Vidraceiro", "Yoga", "Outros"]

    for nome in sorted(categorias):
        if not db.query(models.Categoria).filter_by(nome=nome).first():
            db.add(models.Categoria(nome=nome))
    db.commit()
    db.close()
    print("✅ Banco Perto de Casa SE pronto!")

if __name__ == "__main__":
    popular_sistema()