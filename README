# Mensageria com RabbitMQ e Python

Projeto criado com base no tutorial da documentação do oficial do RabbitMQ. Confira [aqui](https://www.rabbitmq.com/getstarted.html).

## Executando o projeto

Para rodar o projeto copie o arquivo `.env-exemple`, renomeie para `.env` e realize as alterações se desejar.

> As variáveis foram pensadas para o funcionamento com o Docker mas voce pode executar manualmente basta alterar as variaveis ambiente.

A variável `OPERATION_MODE` aceita os seguintes parâmetros:

- PUB_SUB: Para visualizar o funcionamento padrão Publish/Subscribe
- WORK_QUEUES: Para visualizar o funcionamento padrão Work Queues/Task Queues

Demais valores executaram o modo simples de mensageria.

### Subindo os containers

Para subir os containers execute

        docker-compose up

E caso você queira testar com replicações de containers execute

        docker-compose up --build --scale producer=6 --scale consumer=2

Neste caso o compose ira subir 5 containers producers e 2 containers

## Dependências

Dependências de desenvolvimento

```py
pika==1.2.1
pycodestyle==2.8.0
python-dotenv==0.20.0
toml==0.10.2
```
