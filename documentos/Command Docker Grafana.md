# ################### INSTALAÇÃO GRAFANA - DOCKER ###################

# ################### Container Grafana
docker run -d --rm --name grafana -p 3000:3000 -e GF_AUTH_ANONYMOUS_ENABLED=true -e GF_AUTH_ANONYMOUS_ORG_ROLE=Admin grafana/grafana:11.1.3

docker ps

# ################### Conectar no Container p/ Instalar Redis Datasource
docker exec -it grafana bash
grafana cli plugins install redis-datasource
exit

# ################### Reiniciar Container
docker restart grafana
docker ps

# OBS: Se tiver problema com o erro de certificado use --insecure=true.
# Use apenas para desenvolvimento, não use em produção
grafana cli --insecure=true plugins install redis-datasource

# Addres para o Grafana conectar no redis na wsl
host.docker.internal:6379