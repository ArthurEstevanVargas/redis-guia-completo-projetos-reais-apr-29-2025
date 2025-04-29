import redis

# Conexão com o Redis
r = redis.Redis(host='localhost', port=6380, db=0)

# Cria o objeto pubsub
pubsub = r.pubsub()

# Usa o .subscribe() p/ fazer a subscription no topico e escutar por mensagens
pubsub.subscribe('data_channel')

# .listen() retoran um generator que pode ser iterado p/ escutar mensagens do publisher
for message in pubsub.listen():
    print(message) # <-- Você pode aplicar qualquer tratamento de dados aqui (e não apenas imprimir)