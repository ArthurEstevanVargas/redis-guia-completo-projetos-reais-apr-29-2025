# ################################################ INSTALACAO REDIS - DOCKER #################################################

# MOSTRAR DOCKER VAZIO (ELIMINAR IMAGENS SE TIVER ALGO RELACIONADO RODANDO)

# Container para o REDIS
docker run -d --name redis -p 6380:6379 redis

#Checar se container está em execução
docker ps

# Acessar o Redis do Container a partir do host externo
rdcli -u redis://default:666SnngbAeya8QE0YDJOmvXrARuYTuMV@redis-15159.c239.us-east-1-2.ec2.redns.redis-cloud.com:15159
rdcli -h localhost -p 6380
ping
exit

# Acessar o bash no container e acessar o redis internamente no container
docker exec -it redis /bin/bash
redis-cli ping
redis-cli INFO
redis-cli
exit # Sair do redis-cli
exit # Sair do Container Shell

# Acessar o redis no container usando o REDIS INSIGHT

# Parar Container
docker stop redis
docker ps

# Iniciar Container
docker start redis
docker ps

# Reiniciar Container
docker restart redis
docker ps