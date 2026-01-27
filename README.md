# pertodecasa

Ótima escolha! O nome "Perto de Casa" é acolhedor, passa confiança e define perfeitamente a proposta de conectar quem precisa de um serviço com quem mora na região. Para o público sergipano, que valoriza muito a indicação (o famoso "boca a boca"), esse nome cai como uma luva.

Aqui está uma estrutura inicial para tirar o Perto de Casa do papel, focado em prestadores de serviço em Sergipe:

1. A Proposta de Valor
Transformar o "boca a boca" do bairro em uma plataforma digital segura.

Slogan Sugerido: "Perto de Casa: O profissional de confiança do seu bairro."

Dor que resolve: A dificuldade de achar um eletricista, pintor ou diarista confiável e que atenda rápido na sua região (ex: Zona de Expansão, Santos Dumont, ou cidades do interior como Itabaiana e Lagarto).

2. Funcionalidades Principais (O que o app faz)
Para um MVP (Produto Mínimo Viável), foque no essencial:

Busca Geolocalizada Inteligente: O cliente abre o app e vê os profissionais ordenados pela distância (ex: "A 500m de você").

Perfil "Vitrine" do Profissional:

Foto do rosto (gera confiança).

Fotos de "Antes e Depois" dos serviços realizados (essencial para pedreiros, esteticistas, etc.).

Bairros de atendimento (para evitar chamados fora da rota).

Botão "Chamar no Zap": Em Sergipe, negociar pelo WhatsApp é cultural. Não tente criar um chat complexo dentro do app agora; facilite o link direto para o WhatsApp do profissional.

Avaliação por Bairro: "O Eletricista João foi recomendado por 15 vizinhos do Bairro Jardins". Isso valida socialmente o profissional.

3. Categorias Iniciais Sugeridas
Não abra para tudo de uma vez. Foque nas dores urgentes:

Manutenção: Eletricista, Encanador, Pedreiro, Montador de Móveis.

Beleza em Domicílio: Manicure, Cabeleireira, Barbeiro.

Serviços Domésticos: Diarista, Lavadeira, Passadeira.

Técnicos: Manutenção de Celular, Ar-condicionado (muito forte em SE devido ao calor).

4. Diferencial para o Mercado Sergipano
Selo "Verificado": O profissional envia foto do RG e comprovante de residência para ganhar um selo de segurança. Isso combate o medo de colocar estranhos dentro de casa.

Filtro "Atende Agora": Para emergências (ex: cano estourado ou ar-condicionado quebrado no verão).

5. Modelo de Monetização (Como ganhar dinheiro)
Como começar sem afugentar os prestadores (que muitas vezes têm orçamento curto)?

Modelo Freemium (Recomendado): O cadastro básico é grátis.

Plano "Profissional em Destaque" (R$ 19,90/mês):

Aparece no topo das buscas do bairro.

Pode colocar mais fotos no portfólio.

Sem anúncios no perfil dele.

Venda de "Leads" (Opcional futuro): O profissional paga uma pequena taxa para liberar o contato de quem solicitou orçamento (similar ao GetNinjas, mas pode ser complexo para começar).

6. Estratégia de Lançamento (Go-to-Market)
Não tente lançar em Sergipe todo de uma vez.

Estratégia Hiperlocal: Escolha um grande bairro de Aracaju (ex: Augusto Franco ou Jabotiana) ou uma cidade do interior (ex: Nossa Senhora do Socorro).

Campanha: "Você mora no Augusto Franco? Cadastre seu serviço grátis no Perto de Casa".

Parcerias: Fale com síndicos de condomínios. Eles amam ter uma lista de prestadores confiáveis para passar aos moradores. O seu app substitui a "lista de papel" da portaria.

Essa estrutura faz sentido para você?

Se quiser, posso detalhar quais dados precisamos coletar no cadastro (Tabelas do Banco de Dados) para estruturar o sistema.

Como você tem familiaridade com engenharia de dados e Python, estruturei o banco de dados pensando em um modelo relacional (SQL) sólido, pronto para ser implementado com um ORM como SQLAlchemy ou Django.

O foco aqui é a escalabilidade e a inteligência de dados (para garantir que a busca por geolocalização e as métricas de conversão funcionem bem).

Aqui está a modelagem sugerida para o Perto de Casa:

1. Modelo Entidade-Relacionamento (Resumo Lógico)
Usuarios: Tabela base para autenticação (Cliente e Profissional).

Profissionais (Perfil): Extensão do usuário com dados de negócio (Bio, WhatsApp, CNPJ/CPF).

Enderecos: Crucial para a lógica de "Perto de Casa" (Lat/Long + Bairro).

Categorias: Taxonomia dos serviços (ex: Manutenção, Estética).

Portfolio: Galeria de fotos (Antes/Depois).

Analytics (Cliques): Tabela de fatos para registrar quem clicou no WhatsApp (essencial para mostrar valor ao profissional).

2. Detalhamento das Tabelas
Tabela: users (Usuários Base)
Armazena o login e dados comuns.

id (PK, UUID ou BigInt)

full_name (Varchar): Nome de exibição.

email (Varchar, Unique): Para login/recuperação.

password_hash (Varchar): Senha criptografada.

is_provider (Boolean): Flag para distinguir se é cliente ou prestador.

created_at (Timestamp).

Tabela: providers (Perfil do Profissional)
Onde a mágica acontece. Vinculada 1:1 com users.

id (PK)

user_id (FK -> users.id)

whatsapp_number (Varchar): Dado mais crítico do MVP. Apenas números, com DDD (79).

bio (Text): "Sou eletricista há 10 anos, especialista em..."

cpf_cnpj (Varchar): Para validação de segurança (Selo Verificado).

is_verified (Boolean): Se a equipe validou os documentos.

plan_type (Enum): 'FREE', 'PRO', 'DESTAQUE'.

avg_rating (Float): Média de avaliações (cache para não calcular toda vez).

Tabela: addresses (Geolocalização)
Separado do usuário, pois um profissional pode atender em mais de uma base ou mudar de endereço sem afetar o perfil.

id (PK)

user_id (FK -> users.id)

street (Varchar)

number (Varchar)

neighborhood (Varchar): O "Bairro". Essencial para filtros textuais (ex: "Siqueira Campos").

city (Varchar): Ex: Aracaju, Lagarto, Itabaiana.

state (Char 2): Default 'SE'.

zip_code (Varchar): CEP.

latitude (Decimal): Para cálculo de raio (PostGIS ou Haversine).

longitude (Decimal).

Tabela: categories (Taxonomia)
id (PK)

name (Varchar): Ex: "Eletricista", "Manicure".

slug (Varchar): Para URLs amigáveis (ex: perto-de-casa/eletricista).

icon_url (Varchar): Link do ícone do app.

Tabela: provider_services (Relacionamento N:N)
Um "Marido de Aluguel" pode estar em "Encanador" e "Eletricista" ao mesmo tempo.

provider_id (FK -> providers.id)

category_id (FK -> categories.id)

Tabela: portfolio_images (Vitrine)
id (PK)

provider_id (FK -> providers.id)

image_url (Varchar): Caminho no S3/Cloud Storage.

caption (Varchar): Ex: "Instalação de ar split no Bairro 13 de Julho".

type (Enum): 'NORMAL', 'BEFORE', 'AFTER'.

Tabela: interaction_logs (Métricas de Negócio)
Como não teremos chat no MVP, precisamos saber se o app está gerando valor. Contamos os cliques.

id (PK)

provider_id (FK -> providers.id): Quem recebeu o lead.

client_id (FK -> users.id, Nullable): Quem clicou (se estiver logado).

action_type (Enum): 'CLICK_WHATSAPP', 'VIEW_PROFILE', 'SHARE'.

created_at (Timestamp).