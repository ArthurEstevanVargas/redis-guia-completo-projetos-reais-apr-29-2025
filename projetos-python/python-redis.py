"""

MANIPULAÇÃO DE DADOS NO REDIS USANDO PYTHON

Para manipular dados no Redis utilizando Python, você pode usar a bibliotexa redis-py, que fornece uma interface amigável para interagir com o Redis.

Veja aqui os exemplos de como manipular dados nos principais tipos de dados do Redis: hash, list, set e ordered set (sorted set), abordando exemplos práticos para cada um.

Este código demonstra como usar cada um dos tipos de dados no Redis, com exemplos práticos:

- Hash: Armazenamento e recuperação de dados de um usuário.

- List: Gerenciamento de uma lista de tarefas.

- Set: Gerenciamento de um conjunto de tags.

- Ordered Set (Sorted Set): Gerenciamento de uma tabela de classificação de jogadores.

Cada exemplo inclui operações básicas, como adicionar, recuperar, atualizar e remover dados bem como algumas operações específicas para cada tipo de dado.

"""

# Lembre-se de instalar a biblioteca redis-py:
# pip install redis

import redis

# Conexão com o Redis
r = redis.Redis(host='localhost', port=6380, db=0)

#Exemplo de Hash
def hash_example():
    # Adicionando dados ao hash
    r.hset('user:1000', 'name', 'Alice')
    r.hset('user:1000', 'age', 30)
    r.hset('user:1000', 'email', 'alice@exemplo.com')

    # Recuperando dados do hash
    user = r.hgetall('user:1000')
    print(f"Hash - User: {user}")

    # Atualizando um campo no hash
    r.hset('user:1000', 'age', 31)

    # Recuperando um campo específico do hash
    age = r.hget('user:1000', 'age')
    print(f"Update Age: {age}")

# Exemplo de List
def list_example():
    # Adicionando dados à lista
    r.rpush('tasks', 'task1')
    r.rpush('tasks', 'task2')
    r.rpush('tasks', 'task3')

    # Recuperando dados da lista
    tasks = r.lrange('tasks', 0, -1)
    print(f"Exemplo Lista - Tasks: {tasks}")

    # Removendo e retornando o primeiro item da lista
    task = r.lpop('tasks')
    print(f"Popped Task: {task}")

    # Recuperando o tamanho da lista
    size = r.llen('tasks')
    print(f"List Size: {size}")

# Exemplo de Set
def set_example():
    # Adicionando dados ao set
    r.sadd('tags', 'python')
    r.sadd('tags', 'redis')
    r.sadd('tags', 'database')

    # Recuperando todos os membros do set
    tags = r.smembers('tags')
    print(f"Set Example - Tags: {tags}")

    # Verificando a existência de um membro no set
    is_member = r.sismember('tags', 'python')
    print(f"Is 'python' a member of tags? {is_member}")

    # Removendo um membro do set
    r.srem('tags', 'database')

# Exemplo de Ordered Set (Sorted Set)
def sorted_set_example():
    # Adicionando dados ao sorted set
    r.zadd('leaderboard', {'Alice': 100, 'Bob': 200, 'Charlie': 150})

    # Recuperando todos os membros do sorted set com suas pontuações
    leaderboard = r.zrange('leaderboard', 0, -1, withscores=True)
    print(f"Sorted Set Example - Leaderboard: {leaderboard}")

    # Atualizando a pontuação de um membro
    r.zincrby('leaderboard', 50, 'Alice')

    # Recuperando a pontuação de um membro específico
    score = r.zscore('leaderboard', 'Alice')
    print(f"Alice's Update Score: {score}")

    # Recuperando os membros com pontuação entre um intervalo específico
    top_players = r.zrangebyscore('leaderboard', 100, 200, withscores=True)
    print(f"Top Players: {top_players}")

# Executando os exemplos
hash_example()
list_example()
set_example()
sorted_set_example()