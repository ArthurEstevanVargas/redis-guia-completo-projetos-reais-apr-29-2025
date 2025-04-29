# ################################################# TTL #################################################

# O comando TTL (Time to Live) no Redis é usado para gerenciar a expiração de chaves.

# Quando uma chave tem um TTL definido, ela será automaticamente removida do banco de dados após o período especificado.

# Útil para gerenciar dados temporários, cache, sessões de usuário e muito mais.

# EXEMPLOS PRÁTICOS DE USO:

# ############################
# Cache de Respostas de API
# ############################

# Imagine que você está fazendo chamadas para uma API externa e quer armazenar as respostas em cache para reduzir a carga e o tempo de resposta:

# Armazena a resposta da API em cache
FLUSHALL
SET api_response:users "{'users': ['Bruce', 'Clark']}"
GET api_response:users

# Define um TTL de 60 segundos para a chave
# Com isso, a resposta da API será armazenada por 60 segundos.
# Se a mesma requisição for feita novamente dentro desse tempo, a resposta em cache será usada, economizando tempo e recursos.
TTL api_response:users
EXPIRE api_response:users 60
TTL api_response:users

# AO RODAR NOVAMENTE, "RESETA" O TTL:
EXPIRE api_response:users 10
TTL api_response:users

# CHECAR SE A CHAVE FOI REMOVIDA APÓS O TTL ACABAR
GET api_response:users

# ############################
# Gerenciamento de Sessões de Usário
# ############################

# Para aplicativos que requerem autenticação, é comum usar o TTL para gerenciar sessões de usuário, garantindo que as sessões expiradas sejam removidas automaticamente.

# Armazena a sessão do usuário com um TTL de 30 minutos (1800 segundos)
SET session:user1234 "session_data"
GET session:user1234

# Define um TTL de 1800 segundos (30 minutos) para a chave
# Se um usuário estiver inativo por 30 minutos, sua sessão será automaticamente removida
EXPIRE session:user1234 1800
TTL session:user1234
EXPIRE session:user1234 10

# ############################
# Limite de Taxa (Rate Limiting)
# ############################

# O TTL pode ser usado para implementar um sistema de rate limiting, onde você deseja limitar o número de requisições que um usuário pode fazer em um determinado período:
SET requests:user1234 1
GET requests:user1234

# Icrementamos o contador de requisições do usuário
GET requests:user1234
INCR requests:users1234
GET requests:user1234

# Define um TTL de 60 segundos para o contador
# Se o valor do contador exceder um determinado limite, você pode bloquear ou limitar temporariamente o usuário até que o TTL expire.
EXPIRE requests:user1234 10
TTL requests:user1234

# ############################
# Dados Temporários
# ############################

# Em situação onde você precisa armazenar dados temporários, com códigos de verificação ou OTPs (One-Time Passwords), o TTL é essencial!

# Armazenar um código de verificação com um TTL de 5 minutos
SET verification_code:user1234 "123456"
GER verification_code:user1234

# Define um TTL de 300 segundos (5 minutos) para a chave
# Após 5 minutos, o código de verificação será automaticamente removido, garantindo que ele só possa ser usado dentro desse período.
EXPIRE verification_code:user1234 300
TTL verification_code:user1234

# ############################
# Páginação de Resultados
# ############################

# Se você está usando Redis para armazenar resultados de busca paginados, definir um TTL para garantir que os dados sejam removidos após um certo tempo indeterminado, economizando espaço de armazenamento.

# Armazena uma página de resultados de busca
SET search_results:page1 "{'results: ['search1', 'search2']}"
GET search_results:page1

# Define um TTL de 600 segundos (10 minutos) para a chave
# Isso garante que os resultados de busca não sejam mantidos por tempo indeterminado, economizando espaço de armazenamento.
EXPIRE search_results:page1 600
TTL search_results:page1

# ############################
# EXPIRE
# ############################

# Além do EXPIRE, você pode usar o comando TTL para verificar quanto tempo resta antes que uma chave expire:

# PARAMETROS
# NX -- Set expiry only when the key has no expiry
# XX -- Set expiry only when the key has an existing expiry
# GT -- Set expiry only when the new expiry is greater than current one
# LT -- Set expiry only when the new expiry is less than current one

# Insere uma chave e checa o TTL (a chave ainda não tem TTL neste caso)
SET key10 "Infos Data 01"
GET key10
TTL key10

# Seta a expiração apenas quando ja existe um TTL (não é o caso dessa chave, pois ela ainda não tem TTL então não vai setar o TTL)
EXPIRE key10 10 XX
TTL key10

# Seta a expiração quando é p/ configurar um NOVO TTL (como a chave ainda não tinha TTL, o comando vai setar um novo TTL)
DEL key10
SET key10 "Infos Data 01"

EXPIRE key10 45 NX
TTL key10
DEL key10

# ############################
# PERSIST
# ############################

# PERSIST: Remove o TTL de uma chave, tornando-a permanente.
DEL session:user54321
SET session:user54321 "54321"
GET session:user54321

EXPIRE session:user54321 60
TTL session:user54321

PERSIST session:user54321
TTL session:user54321