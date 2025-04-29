import redis

# Conexão com o Redis
r = redis.Redis(host='localhost', port=6380, db=0)

while True:
    message = input("REALTIME PUSH NOTIFICATION - Digite a Mensagem: ")
    r.publish("data_channel", message)