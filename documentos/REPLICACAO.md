# Checar Path do Arquivo de Configuração do Redis
# config_file:/opt/homebrew/etc/redis.conf
redis-cli INFO | grep config_file

# REINICIAR REDIS
sudo service redis-server start
sudo service redis-server stop

# 3. CRIAR PASTAS
mkdir -p ~/downloads
cd ~/downloads
mkdir -p redis-replication
cd redis-replication
mkdir -p master replica1 replica2

# 4. LISTAR PASTAS CRIADAS
ls -lrth

# COPIAR ARQUIVOS DE CONFIGURAÇÃO
sudo cp /etc/redis/redis.conf ~/downloads/redis-replication/master/redis-master.conf
sudo cp /etc/redis/redis.conf ~/downloads/redis-replication/replica1/redis-replica1.conf
sudo cp /etc/redis/redis.conf ~/downloads/redis-replication/replica2/redis-replica2.conf

# DATA DIRECTORY
mkdir -p ~/downloads/redis-replication/master/data
mkdir -p ~/downloads/redis-replication/replica1/data
mkdir -p ~/downloads/redis-replication/replica2/data

# AJUSTAR AS CONFIGURAÇÕES
# Master - Muda apenas a porta (ou manter padrão)
# Replicas - Mudar a porta, data directory e logfile

# 6231 master
# 6232 slave
# 6233 slave

# Master
sudo vi ~/downloads/redis-replication/master/redis-master.conf

port 6231
logfile /home/arthur/downloads/redis-replication/master/redis-master.log
dir /home/arthur/downloads/redis-replication/master/data

# =======

sudo vi ~/downloads/redis-replication/replica1/redis-replica1.conf

port 6232
logfile /home/arthur/downloads/redis-replication/replica1/redis-replica1.log
dir /home/arthur/downloads/redis-replication/replica1/data

# =======

sudo vi ~/downloads/redis-replication/replica2/redis-replica2.conf

port 6233
logfile /home/arthur/downloads/redis-replication/replica2/redis-replica2.log
dir /home/arthur/downloads/redis-replication/replica2/data

# =======

# ABRIR TERMINAIS SEPARADOS

# Iniciar Servidor - REDIS MASTER
sudo redis-server ~/downloads/redis-replication/master/redis-master.conf 
sudo tail -f ~/downloads/redis-replication/master/redis-master.log

# Iniciar Servidor - REDIS REPLICA1
sudo redis-server ~/downloads/redis-replication/replica1/redis-replica1.conf
sudo tail -f ~/downloads/redis-replication/replica1/redis-replica1.log

# Iniciar Servidor - REDIS REPLICA2
sudo redis-server ~/downloads/redis-replication/replica2/redis-replica2.conf
sudo tail -f ~/downloads/redis-replication/replica2/redis-replica2.log

# CHECAR INFORMAÇÕES DE REPLICAÇÃO NO MASTER
redis-cli -p 6231
info replication
exit

# CONECTAR NA REPLICA1 E REPLICA2 E CONFIGURAR REPLICAÇÃO MASTER

# REPLICA 1
redis-cli -p 6232
replicaof 127.0.0.1 6231
exit

# REPLICA 2
redis-cli -p 6233
replicaof 127.0.0.1 6231
exit

# MOSTRAR INFOS DAS REPLICAS LISTANDO AS OPÇÕES NO MASTER
# INSERIR CHAVE NO MASTER

redis-cli -p 6231
info replication

set usuario:123 bruce
exit

# CHECAR NA REPLICA1 SE A CHAVE ESTÁ DISPONÍVEL
redis-cli -p 6232
get usuario:123
exit

# CHECAR NA REPLICA1 SE A CHAVE ESTÁ DISPONÍVEL
redis-cli -p 6233
get usuario:123
exit

# ATUALIZAR CHAVE NO MASTER
redis-cli -p 6231
set usuario:123 "bruce wayne"
exit

# CHECAR NA REPLICA1 SE A CHAVE ESTÁ DISPONÍVEL
redis-cli -p 6232
get usuario:123
exit

# OBS.
# Por padrão, apenas é possível escrever no master e as réplicas são somente para leitura.
# Se tentarmos escrever em uma réplica, ocorrerá um erro:
# (error) READONLY You can't write against a read only replica.
redis-cli -p 6232
set usuario:123 "Clark"
exit