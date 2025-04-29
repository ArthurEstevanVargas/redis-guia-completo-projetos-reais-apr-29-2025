# == Usando o Recurso de Publisher/Subscriber (Pub/Sub) do Redis

# Comandos Principais do Pub/Sub

- PUBLISH: Envia uma mensagem para um canal

- SUBSCRIBE: Inscreve o cliente em um ou mais canais.

- UNSUBSCRIBE: Cancela a inscrição do cliente em um ou mais canais.

- PSUBSCRIBE: Cancela a inscrição do cliente em um ou mais padrões de canais.

- PUNSUBSCRIBE: Cancela a inscrição do cliente em um ou mais padrões de canais.

- PUBSUB: Exibe informações sobre o sistema Pub/Sub.

# === Exemplo Prático: Sistema de Notificações em Tempo Real

Vamos criar um exemplo prático de um sistema de notificações em tempo real usando o Pub/Sub do Redis. Imagine que temos um sistema de gerenciamento de tarefas onde os usuários precisam ser notificados em tempo real sobre mudanças nas tarefas.

Passo 1: Configurações do Ambiente
Para este exemplo, utilizaremos duas sessoes de clientes Redis: uma para o publicador e outra para o assinante.

Passo 2: Implementação do Subscriber
Primeiro, vamos configurar o assinante para ouvir notificações em um canal chamado task_updates.

Subscriber 1:
redis-cli

SUBSCRIBE task_updates

Passo 3: Implementação do Publicador
Em seguida, vamos configurar o publicador para enviar mensagens para o canal task_updates sempre que houver uma atualização de tarefa.

Publisher 1:
redis-cli

PUBLISH task_updates "Tarefa 123 foi atualizada"
PUBLISH task_updates "Tarefa 456 foi atualizada"

# === Exemplo Prático: Sistema de Chat em Tempo Real

Vamos agora criar um exemplo de um sistema de chat em tempo real, onde os usuários podem enviar e receber mensagens instantaneamente.

Passo 1: Configurações do Ambiente
Para este exemplo, utilizaremos três sessões de cliente Redis: uma para publisher e duas para o subscribers.

Passo 2: Implementação dos Assinantes
Primeiro, vamos configurar os assinantes para ouvir mensagens em um canal chamado chat_room.

Subscriber 1:
redis-cli

SUBSCRIBE chat_room

Subscriber 2:
redis-cli

SUBSCRIBE chat_room

Passo 3: Implementação do Publisher
Em seguida, vamos configurar o publicador para enviar mensagens para o canal chat_room.

Publisher:
redis-cli

PUBLISH chat_room "Olá a todos! Bem vindos ao chat."
PUBLISH chat_room "Bye Bye"

Ambos os assinantes receberão a mensagem


# === Exemplo Prático: Sistema de Alerta em Tempo Real

Vamos criar um exemplo de um sistema de alerta em tempo real, onde os serviços podem enviar alertas críticos que precisam ser distribuídos para múltiplos assinantes imediatamente.

Passo 1: Configuração do Ambiente
Para este exemplo, utilizaremos duas sessões de Cliente Redis: uma para o publicador e outra para o assinante.

Passo 2: Implementação do Subscriber
Primeiro, vamos configurar o subscriber para ouvir alertas em um canal chamado critical_alerts.

Subscriber:
redis-cli

SUBSCRIBE critical_alerts

Passo 3: Implementação do Publisher
Em seguida, vamos configurar o publicador para enviar mensagens para o canal critical_alerts sempre que houver um alerta crítico.

Publisher:
redis-cli

PUBLISH critical_alerts "Alerta crítico: o servidor está inativo."
PUBLISH critical_alerts "Alerta crítico: nada está funcionando."

# === Monitorando e Gerenciando Pub/Sub

O comando PUBSUB fornece informações úteis sobre o sistema Pub/Sub, incluindo o número de assinantes em um canal e os padrões de canais.

Exemplo
redis-cli

PUBSUB channels

Exemplo:
redis-cli
PUBSUB numsub task_updates
PUBSUB numsub chat_room
PUBSUB numsub critical_alerts