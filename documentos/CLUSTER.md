### ############################################################
### REDIS CLUSTER
### ############################################################


# Vamos inicializar algumas instancia do redis e configurá-las para rodar o REDIS no CLUSTER MODE

# Segue um exemplo de configuração mínima para rodar o REDIS CLUSTER

# cluster-enabled: Rodar no CLUSTER MODE

# cluster-config-file: Define o nome do arquivo onde a configuração deste nó é armazenada, em caso de reinicialização do servidor.

# cluster-node-timeout: número de milissegundos que um nó deve ficar inacessível para ser considerado em estado de falha.

# CRIAR PASTAS
mkdir ~/downloads/redis-cluster
cd ~/downloads/redis-cluster

# CRIAR Primeiro Arquivo redis.conf
sudo vi redis-cluster-original.conf

port 7001
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes

### ############################################################
### CRIAR 3 "PRIMARY SHARDS" E 3 RÉPLICAS (1 P/ CADA PRIMARY)
### ############################################################

# AO FINAL, TEREMOS 6 INSTÂNCIAS DO REDIS (3 PRIMARY / 3 RÉPLICAS)
# OBS: EM PRODUÇÃO, SEMPRE USE 2 RÉPLICAS P/ CADA PRIMARY, PARA SE PROTEGER CONTRA O "SPLIT BRAIN".

# CRIAR 6 DIRETORIOS PARA CADA ARQUIVO DE CONFIGURAÇÃO E COPIAR O ARQUIVO DE CONFIGURAÇÃO PARA CADA PASTA
cd ~/downloads/redis-cluster
mkdir -p {7001..7006}
ls -l
for i in {7001..7006}; do cp ~/downloads/redis-cluster/redis-cluster-original.conf $i/redis.conf; done
for i in {7001..7006}; do echo $i; ls -l $i; done

# MUDAR A PORTA EM CADA UM DOS ARQUIVOS DE CONFIGURAÇÃO
sudo vi ~/downloads/redis-cluster/7001/redis.conf
sudo vi ~/downloads/redis-cluster/7002/redis.conf
sudo vi ~/downloads/redis-cluster/7003/redis.conf
sudo vi ~/downloads/redis-cluster/7004/redis.conf
sudo vi ~/downloads/redis-cluster/7005/redis.conf
sudo vi ~/downloads/redis-cluster/7006/redis.conf

# CHECAR SE OS ARQUIVOS FORAM MODIFICADOS CORRETAMENTE
for i in {7001..7006}; do echo "~/downloads/redis-cluster/$i/redis.conf"; cat ~/downloads/redis-cluster/$i/redis.conf; done

# INICIALIZAR OS 6 SERVIDORES (1 EM CADA ABA)
# TAB1
cd ~/downloads/redis-cluster/7001
redis-server redis.conf

# TAB2
cd ~/downloads/redis-cluster/7002
redis-server redis.conf

# TAB3
cd ~/downloads/redis-cluster/7003
redis-server redis.conf

# TAB4
cd ~/downloads/redis-cluster/7004
redis-server redis.conf

# TAB5
cd ~/downloads/redis-cluster/7005
redis-server redis.conf

# TAB6
cd ~/downloads/redis-cluster/7006
redis-server redis.conf

# COM AS 6 INSTÂNCIAS, VAMOS INICIALIZÁ-LAS EM UM CLUSTER 

# O redis-cli vai propor uma configuração; aceite-a digitando yes.

# O cluster será configurado e as instância serão inicializadas para se comunicar umas com as outras.

# --cluster-replicas: Informa quantas REPLICAS cada PRIMARY vai ter

# Você deve ver a seguinte mensagem ao final:
# [OK] All 16384 slots covered

redis-cli --cluster create \
127.0.0.1:7001 \
127.0.0.1:7002 \
127.0.0.1:7003 \
127.0.0.1:7004 \
127.0.0.1:7005 \
127.0.0.1:7006 \
--cluster-replicas 1

### ############################################################
### CHECAR AS CONFIGURAÇÕES DO CLUSTER
### ############################################################

# Verificar o estado do cluster, use o comando:
redis-cli -p 7001 cluster info

# Listar os nós e suas funções:
redis-cli -p 7001 cluster nodes

# CHECAR A DISTRIBUIÇÃO DOS HASHLOTS
redis-cli -p 7001 cluster slots

### ############################################################
### ADICIONAR UM NOVO "SHARD" NO CLUSTER
### ############################################################

# ESSA É UMA FORMA DE ESCALAR O CLUSTER REDIS:
# ARQUITETURA PARA ADICIONAR NOVOS SERVIDORES PRIMARY E REPLICAS

# INICIAR 2 NOVAS INSTANCIA REDIS: O NOVO PRIMARY E SUA REPLICA

# CRIAR AS PASTAS
# COPIAR OS NOVOS ARQUIVOS DE CONFIGURAÇÃO
# AJUSTAR A CONFIGURAÇÃO DA PORTA EM CADA ARQUIVO (7006 E 7007)

cd ~/downloads/redis-cluster
ls -l

mkdir 7007 7008

cp 7001/redis.conf 7007/redis.conf
ls 7007/redis.conf

cp 7001/redis.conf 7008/redis.conf
ls 7008/redis.conf

# AJUSTAR A PORTA DOS 2 NOVOS SERVERS
sudo vi 7007/redis.conf
sudo vi 7008/redis.conf

# CHECAR SE AS PORTAS ESTÃO CONFIGURADAS CORRETAMENTE
sudo cat 7007/redis.conf
sudo cat 7007/redis.conf

# INICIALIZAR AS 2 NOVAS INSTÂNCIAS DO REDIS

# TAB7
cd ~/downloads/redis-cluster/7007
redis-server redis.conf

# TAB8
cd ~/downloads/redis-cluster/7008
redis-server redis.conf

### ############################################################
### ADICIONAR UM NOVO NÓ PRIMARY NO CLUSTER
### ############################################################

# PARÂMETROS:
# PRIMEIRO ESPECIFICAMOS O NOVO SHARD (PRIMARY) E EM SEGUIDA O ENDEREÇO DE QUALQUER OUTRO SHARD DO CLUSTER

# NOVA TAB:
redis-cli --cluster add-node 127.0.0.1:7007 127.0.0.1:7001

### ############################################################
### CHECAR NOVAMENTE AS CONFIGURAÇÕES DO CLUSTER
### ############################################################

# Verificar o estado do cluster, use o comando:
redis-cli -p 7001 cluster info

# Listar os nós e suas funções:
redis-cli -p 7001 cluster nodes

# CHECAR A DISTRIBUIÇÃO DOS HASHLOTS
redis-cli -p 7001 cluster slots

### ############################################################
### ADICIONAR A NOVA REPLICA NO CLUSTER
### ############################################################

# NO CASO DA REPLICA, PRECISAMOS ESPECIFICAR ALGUNS PARAMETROS EXTRA:

# - O SERVIDOR REPLICA QUE SERÁ ACRESCENTADO NO CLUSTER

# - QUAL SHARD PRIMARY SERÁ USADO PELA REPLICA PARA REPLICAR OS DADOS
# (SE NÃO ESPECIFICARMOS, O REDIS VAI ATRIBUIR UM SERVIDOR PRIMARY ARBITRÁRIO.)

# ATENÇÃO!!!
# CHECAR OS IDS DOS SHARDS E TOMAR NOTA DO ID SHARD QUE ESTA RODANDO NA PORTA 7007
# (POIS É O NOVO SHARD/PRIMARY QUE ADICIONAMOS E QUE SERÁ UTILIZADO PELA RÉPLICA PARA REPLICAR OS DADOS):
redis-cli -p 7001 cluster nodes

# ADICIONAR O NOVO SERVER REPLICA:

# INFORMAÇÕES SOBRE OS PARÂMETROS:

# --cluster add-node
# INFORMA QULA NÓ SERÁ ADICIONADO NO CLUSTER E INFORMA UM SHARD DO CLUSTER

# --cluster-slave
# INDICA QUE O SHARD DEVE PARTICIPAR DO CLUSTER COMO UMA RÉPLICA

# --cluster-master-id
# Especifica qual PRIMARY SHARD a réplica deve replicar

# ATENÇÃO:
# AJUSTART O ID PARA QUE A NOSSA REPLICA (7008) APONTAR P/ O MASTER ID CORRETO (7007 NESTE NOSSO EXEMPLO)!
redis-cli \
-p 7001 \
--cluster add-node 127.0.0.1:7008 127.0.0.1:7001 \
--cluster-slave --cluster-master-id 080f4341cad787dbfb3a825df2a81dc8a3c351cc

# OBS:
# SE TENTAR ADICIONAR UM NÓ QUE JÁ TENHA SIDO INICIALIZADA, VAI APRESENTAR O ERRO
# [ERR] Node 127.0.0.1:7007 is not empty. Either the node already knows other nodes (check with CLUSTER NODES) or contains some key in database 0.

### ############################################################
### FAZER O RESHARD PARA QUE O NOVO PRIMATY SERVER POSSA RECEBER HASHSLOTS
### ############################################################

# INFORMAR A QTDE DE SLOTS A MOVER
# COMO SÃO 4 PRIMARY, DIVIDIR: 16384 / 4 = 4096

# INFORMAR O ID DO SHARD PRIMARIO PARA ONDE QUEREMOS MOVER OS DADOS

# INFORMAR O ID DO SHARD DE ONDE QUEREMOS COPIAR OS DADOS (INFORMAR "ALL" E O REDIS VAI MOVER ALGUNS HASHSLOTS DE TODOS OS PRIMARY DISPONÍVEIS)

redis-cli -p 7001 --cluster reshard 127.0.0.1:7001
# 4096
# USAR O MESMO ID DA INSTANCIA 7007 QUE ANOTAMOS ANTERIORMENTE
# all
# yes

### ############################################################
### USANDO O REDIS-CLI COM UM REDIS CLUSTER
### ############################################################

# Quando você usa o redis-cli para se conectar a um shard de um Redis Cluster, você é conectado somente a esse shard e não pode acessar dados de outros shard!

# Se você tentar acessar chaves do shard errado, você receberá um erro "MOVED".

# Há um truque para usar o redis-cli para não ter que abrir conexão para todos os shards, mas em vez disso você deixa que ele faça o trabalho de conectar e reconectar para você.

# É o modo do suporte de cluster do redis-cli, usando -c:
# Com isso, Quando usarmos o REDIS no modo cluster, se o cliente receber uma resposta de erro "MOVED 15495 127.0.0.1:7002" do shard ao qual está conectado, ele simplesmente se reconectará ao endereço retornado na resposta de erro, neste caso "127.0.0.1:7002".

# TESTAR CONEXÃO: SEM HABILITAR O MODO CLUSTER
redis-cli -p 7001

get usuario:123
# (erro) MOVED num 127.0.0.1:7007

get pagamento:456
# (erro) MOVED num 127.0.0.1:7003

get produto:789
# (erro) MOVED num 127.0.0.1:7003

# TESTAR CONEXÃO: HABILITANDO O MODO CLUSTER
redis-cli -p 7001 -c

get usuario:123
# -> Redirected to slot [num] located 127.0.0.1:7007

get pagamento:456
# -> Redirected to slot [num] located 127.0.0.1:7003

get produto:789
# -> Redirected to slot [num] located 127.0.0.1:7003
