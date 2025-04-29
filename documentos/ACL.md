# == SEGURANÇA NO REDIS

Comandos Básicos de ACL

Os principais comandos relacionados a ACLs no Redis são:

-- ACL SETUSER: Cria ou modifica um usuário.
-- ACL DELUSER: Remove um usuário.
-- ACL LIST: Lista todos os usuários e suas permissões.
-- ACL SAVE: Salva as configurações de ACL no disco.
-- ACL LOAD: Carrega as configurações de ACL do disco.
-- ACL LOG: Exibe o log de eventos de segurança relacionados a ACL.
-- ACL WHOMI: Retorna o nome do usuário atual.

# FLUSHALL

Criando e Gerenciando Usuários com ACLs

Criando um Usuário

Para criar um usuário com permissões específicas, use o comando ACL SETUSER.

Exemplo:
ACL SETUSER bruce on >password ~* +@all
clear
ACL LIST

Neste exemplo, estamos criando um usuário chamado bruce:
on: Habilita o usuário.

>password: Define a senha do usuário

~*: Permite acesso a todas as chaves.

+@all: Concede permissão para todos os comados.

Restrigindo Permissões
Podemos criar um usuário com permissões mais restritas.

Exemplo:
ACL SETUSER bob on >securepassword ~cache:* +get +set
clear
ACL LIST

Neste exemplo, o usuário bob tem as seguintes permissões:
- Acesso apenas a chaves que começam com cache:
- Permissões para executar apenas os comandos GET e SET

Listando Usuários e Permissões
Para listar todos os usuários e suas permissões, use o comando ACL LIST.

Exemplo:
clear
ACL LIST

Removendo um Usuário
Para remover um usuário, use o comando ACL DELUSER

ACL DELUSER bruce
clear
ACL LIST

ACL DELUSER bob
clear
ACL LIST

# === Configurando ACLs para Diferentes Cenários REAIS

Cenário 1: Criar um usuário que só pode executar comandos de leitura, como o GET.

ACL SETUSER readonly on >readonlypassword ~* +get
clear
ACL LIST

Cenário 2: Criar um usuário que só pode executar comandos de escrita, como SET.

ACL SETUSER writeonly on >writeonlypassword ~* +set
clear
ACL LIST

Cenário 3: Usuário com Acesso Restrito a Comandos e Chaves Específicas.

ACL SETUSER restricted on >restrictedpassword ~data:* +get +set
clear
ACL LIST

# === Exemplo Completo de ACL (Configuração de ACL persistindo os dados no disco)

# Limpar as Configurações para Realizar o Teste
sudo vi /etc/redis/redis.conf

# Procurar e Remover Linha
aclfile /etc/redis/users.acl

# Remover arquivo com ACLs
rm /etc/redis/users.acl

# Reiniciar serviço e fazer login para testar se serviço está funcionando OK
sudo service redis-server stop
sudo service redis-server start
redis-cli
ping
exit

# Vamos considerar um cenário onde temos diferentes tipo de usuários com diferentes permissões

# Passo 1: Configurações Inicial no redis.conf Adicione a linha para especificar o arquivo de ACLs:

# ATUALIZAR CONFS DO REDIS
sudo vi /etc/redis/redis.conf

# Procurar no arquivo de confs a linha comentada e ajustar pro seu path:
aclfile /etc/redis/users.acl

# Atualizar o Path de acordo com a sua instalação:
acfile /etc/redis/users.acl

# OBS:
# Ex de Path no Linux:
# acfile /etc/redis/users.acl

# Passo 2: Criação do Arquivo users.acl
# Crie e edite o arquivo de ACL com o seguiente conteúdo:

sudo vi /etc/redis/users.acl

user default on nopass ~* +@all
user ze on >password ~* +@all
user chico on >securepassword ~cache:* +get +set
user appleitura on >readonlypassword ~* +get
user appescrita on >writeonlypassword ~* +set
user apprestrito on >restrictedpassword ~data:* +get +set

sudo cat /etc/redis/users.acl

# Passo 3: Reinicie o Redis para carregar as configurações do arquivo de ACL
sudo service redis-server stop
sudo service redis-server start
redis-cli
ping
exit

# Passo 4: Faço o Login usando o usuário default e liste os usuários disponíveis (deverão ser listados os usuários)
redis-cli
clear ACL LIST

# Passo 5: Uma vez com a ACL configurada, testar criar novo usuário, salvar a ACL em disco, reiniciar o redis e logar com o novo usuário.

# Se tudo correr bem, teremos a certeza que o Redis estpa persistindo as informações no arquivo de ACL e as informações ficarão a salvo mesmo quando o redis reiniciar e limpar a memória.

# Criar Novo Usuário
ACL SETUSER appuser on >mypass ~app:* +get +set

# Salvar ACL
# Se tudo correr bem, não irá gerar erro:
ACL SAVE

# Reiniciar o Redis
exit
sudo service redis-server stop
sudo service redis-server start
redis-cli
ping
exit

# Passo 6: Fazer o Login usando o usuário recém criado e usuário da ACL
redis-cli -h localhost -p 6379 --user appuser --pass 'mypass'

# Veja se gera um erro de permissão
# (erro) NOPERM No permissions to access a key
set user:12345 newinfo

# Testar com uma chave que dá acesso:
set app:12345 newinfo
get app:12345

exit

# OUTRA FORMA DE AUTENTICAR COM OS NOVOS USUÁRIOS, SE JÁ ESTIVER CONECTADO NO CONSOLE
auth appleitura 'readonlypassword'

# Vai funcionar:
get app:12345

# Vai gerar erro, pois o usuário não possui permissão de escrita
set app:54321 newinfo54321

# PARA SALVAR AS SENHAS DE FORMA SEGURA USE "SHA-256"!

# Use o formato: #<hash> para especificar a senha
# "hash" deve ser substituido pelo hash SHA-256 da senha
# Este valor de hash será comparado ao hash da senha inserida para um usuário ACL

# Isso permite que os usuários armazenem  hashes no arquivo de ACL ao invés de armazenar senhas em texto simples
# Apenas valores de hash SHA-256 são aceitos: o hash da senha deve ter 64 caracteres e conter apenas caracteres hexadecimal minúsculos

sudo vi /etc/redis/users.acl
user ze on #5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 ~* +@all