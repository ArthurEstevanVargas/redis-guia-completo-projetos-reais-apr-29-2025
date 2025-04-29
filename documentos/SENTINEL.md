# ################################################################
# REDIS SENTINEL
# ################################################################


# ################################################################
# CRIAR WORKING DIRECTORY
# ################################################################
mkdir -p ~/downloads/redis-replication/sentinel1
mkdir -p ~/downloads/redis-replication/sentinel2
mkdir -p ~/downloads/redis-replication/sentinel3

mkdir -p ~/downloads/redis-replication/sentinel1/data
mkdir -p ~/downloads/redis-replication/sentinel2/data
mkdir -p ~/downloads/redis-replication/sentinel3/data

ls -lrth

# ################################################################
# ARQUIVOS DE CONFIGURAÇÃO DO SENTINEL (sentinel.conf)
# ################################################################
# SENTINELA 1 - RODANDO NA PORTA 7231
sudo vi ~/downloads/redis-replication/sentinel1/sentinel1.conf

port 7231
sentinel monitor mymaster 127.0.0.1 6231 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
dir "/home/arthur/downloads/redis-replication/sentinel1/data"

# SENTINELA 2 - RODANDO NA PORTA 7231
sudo vi ~/downloads/redis-replication/sentinel2/sentinel2.conf

port 7232
sentinel monitor mymaster 127.0.0.1 6231 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
dir "/home/arthur/downloads/redis-replication/sentinel2/data"

# SENTINELA 3 - RODANDO NA PORTA 7231
sudo vi ~/downloads/redis-replication/sentinel3/sentinel3.conf

port 7233
sentinel monitor mymaster 127.0.0.1 6231 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
dir "/home/arthur/downloads/redis-replication/sentinel3/data"

# ################################################################
# INICIALIZANDO SENTINELS
# ################################################################

sudo redis-sentinel ~/downloads/redis-replication/sentinel1/sentinel1.conf
sudo redis-sentinel ~/downloads/redis-replication/sentinel2/sentinel2.conf
sudo redis-sentinel ~/downloads/redis-replication/sentinel3/sentinel3.conf

# ################################################################
# APÓS INICIAR CADA SENTINEL, O ARQUIVO DE CONFIGURAÇÃO SERÁ ATUALIZADO DE ACORDO:
# ################################################################

# sentinel monitor mymaster 127.0.0.1 6231 2
# sentinel known-replica mymaster 127.0.0.1 6232
# sentinel known-replica mymaster 127.0.0.1 6233

cat ~/downloads/redis-replication/sentinel1/sentinel1.conf
cat ~/downloads/redis-replication/sentinel2/sentinel2.conf
cat ~/downloads/redis-replication/sentinel3/sentinel3.conf

# ################################################################
# REALIZANDO UM FAILOVER
# ################################################################

# PARA REALIZAR UM FAILOVER, VAMOS MANUALMENTE PARAR O SERVIDOR MASTER
# COM ISSO, A ELEIÇÃO DE UM NOVO MASTER OCORRERÁ LOGO EM SEGUIDA (VER LOGS DO SENTINEL)
redis-cli -p 6231
SHUTDOWN
exit

# ################################################################
# CHECAR OUTPUT/LOGS DOS SENTINELS APÓS O FAILOVER
# ################################################################

# MASTER MUDOU DO REDIS 6231 PRO REDIS 6233
# REPLICA 2 SE TORNOU O NOVO MASTER
# +switch-master mymaster 127.0.0.1 6231 127.0.0.1 6232

# +slave slave 127.0.0.1:6233 127.0.0.1 6233 @ mymaster 127.0.0.1 6232
# +slave slave 127.0.0.1:6231 127.0.0.1 6231 @ mymaster 127.0.0.1 6232

# ################################################################
# TESTAR SE AGORA É POSSÍVEL ESCREVER NO NOVO MASTER
# ################################################################
redis-cli -p 6232
set newuser:12345 "Clark"
exit

# ################################################################
# CONECTAR EM UMA RÉPLICA
# TENTAR INSERIR UMA CHAVE (VAI GERAR ERRO)
# LER A NOVA CHAVE INSERIDA P/ CONFIRMAR QUE A REPLICAÇÃO ESTÁ FUNCIONANDO
# ################################################################

redis-cli -p 6233
set newuser:1234567 "Mark"
get newuser:12345

# ################################################################
# CHECAR CONFS DOS SENTINELS APÓS FAILOVER
# ################################################################
cat ~/downloads/redis-replication/sentinel1/sentinel1.conf
cat ~/downloads/redis-replication/sentinel2/sentinel2.conf
cat ~/downloads/redis-replication/sentinel3/sentinel3.conf

# ################################################################
# SE INICIARMOS NOVAMENTE O ANTIGO MASTER, ELE VAI AGORA SE TORNAR UMA RÉPLICA (DO NOVO MASTER)
# ################################################################

# Iniciar Servidor - REDIS MASTER
sudo redis-server ~/downloads/redis-replication/master/redis-master.conf 
sudo tail -f ~/downloads/redis-replication/master/redis-master.log

# +convert-to-slave slave 127.0.0.1:6231 127.0.0.1 6231 @ mymaster 127.0.0.1 6232

ps aux | grep redis-server