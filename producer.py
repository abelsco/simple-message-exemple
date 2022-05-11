#!.venv/bin python
"""
Código que implementa um produtor de mensagens para o RabbitMQ

### Clases
 - MensageriaSimples: Padrão de envio simples por um canal e fila
 - PubSub: Padrão de envio Publisher/Subscriber
"""
import os
import random
import json
import sys
from dotenv import load_dotenv
import pika


def definicao_env():
    """
    Função que realiza a carga das variáveis de ambiente e retorna um dicionário

    ### Chaves do dicionário
        - user: Usuário de acesso ao RabbitMQ
        - passwd: Senha de acesso ao RabbitMQ
        - server: Endereço do servidor RabbitMQ
        - port: Porta exposta do servidor RabbitMQ
        - queue: Nome da fila do RabbitMQ
        - exchange: Nome da exchange do RabbitMQ
        - rounds: Define quantas requisições serão feitas ao RabbitMQ

    ### Retorno
        _dict_: Dicionário com as variáveis definidas
    """
    # Carrego as variaveis
    load_dotenv()
    # Defino o dicionário com as variaveis do meu ambiente
    config = {
        "user": os.getenv("RABBITMQ_USER"),
        "passwd": os.getenv("RABBITMQ_PASS"),
        "server": os.getenv("RABBITMQ_SERVER"),
        "port": os.getenv("RABBITMQ_PORT"),
        "queue": os.getenv("RABBITMQ_NAME_QUEUE"),
        "exchange": os.getenv("RABBITMQ_NAME_EXCHANGE"),
        "rounds": int(os.getenv("MAX_RUNS")),
    }
    return config


def gerador_nome_completo():
    """
    Função geradora de nomes pseudoaleatórios

    ### Retorno
        _str_: Nome completo
    """
    # Inicializo o ambiente com uma nova seed
    random.seed()
    nome = (
        "Maria",
        "Jose",
        "Ana",
        "Joao",
        "Antonio",
        "Francisco",
        "Carlos",
        "Paulo",
        "Pedro",
        "Lucas",
        "Luiz",
        "Marcos",
        "Luis",
        "Gabriel",
        "Rafael",
        "Francisca",
        "Daniel",
        "Marcelo",
        "Bruno",
        "Eduardo"
    )
    particula = (" de ", " da ", " do ", " ")
    sobrenome = ("Jesus", "Menezes", "Silva", "Oliveira", "Matos", "Meneses")
    return str().join(random.sample(nome, 1) +
                      random.sample(particula, 1) + random.sample(sobrenome, 1))


def simula_dados_api():
    """
    Função serializadora de JSON que simula dados populados por uma API

    Returns:
        _str_: Dados serializados
    """
    # Inicializo o ambiente com uma nova seed
    random.seed()
    api = [{
        "status": 200,
        "data": {
            "name": gerador_nome_completo(),
            "pedido_id": random.sample(range(100), 1),
            "cartao": {
                "valor": random.sample(range(100), 1),
                "parcelas": random.sample(range(10), 1),
                "bandeira": "We gonna be ok",
                "num": random.sample(range(1000, 5000), 4),
                "cvv": random.sample(range(100, 300), 1)
            }
        }
    }]
    return json.dumps(api)


class MensageriaSimples:
    """
    ## Mensageria Simples

    Classe que implementa a troca de mensagens com o RabbitMQ
    atraves de uma canal e uma fila pré estabelicida

    #### Métodos

    - abrir_conexao(self)
    - envia_mensagem(self)
    """

    def __init__(self):
        self.config = definicao_env()
        self.conexao = self.abrir_conexao()
        self.canal = self.conexao.channel()
        self.envia_mensagem()

    def abrir_conexao(self):
        """
        Método que retorna a conexão criada

        Returns:
            _BlockingConnection_: Objeto de conexão da biblioteca pika
        """
        credenciais = pika.PlainCredentials(
            self.config["user"], self.config["passwd"])
        conexao = pika.BlockingConnection(pika.ConnectionParameters(
            self.config["server"], self.config["port"], '/', credenciais))
        return conexao

    def envia_mensagem(self):
        """
        Método de envio de mensagens ao RabbitMQ pelo canal e fila
        """
        self.canal.queue_declare(queue=self.config["queue"])
        # Roda o laço rounds vezes simulando o envio de varias mensagens serializadas
        for _ in range(self.config["rounds"]):
            dados = simula_dados_api()
            self.canal.basic_publish(exchange='', routing_key=self.config["queue"],
                                     body=dados)
            print(f"[x] Enviando '{dados}'")

        self.conexao.close()


class PubSub:
    """
    ## Mensageria Simples

    Classe que implementa a troca de mensagens com o RabbitMQ
    no padrão Pub/Sub onde as mansegens são enfileiradas para varios consumidores
    atravez da exchange

    #### Métodos

    - abrir_conexao(self)
    - envia_mensagem(self)
    """

    def __init__(self):
        self.config = definicao_env()
        self.conexao = self.abrir_conexao()
        self.canal = self.conexao.channel()
        self.envia_mensagem()

    def abrir_conexao(self):
        """
        Método que retorna a conexão criada

        Returns:
            _BlockingConnection_: Objeto de conexão da biblioteca pika
        """
        credenciais = pika.PlainCredentials(
            self.config["user"], self.config["passwd"])
        conexao = pika.BlockingConnection(pika.ConnectionParameters(
            self.config["server"], self.config["port"], '/', credenciais))
        return conexao

    def envia_mensagem(self):
        """
        Método de envio de mensagens ao RabbitMQ atraves da exchange
        """
        self.canal.exchange_declare(
            exchange=self.config["exchange"], exchange_type='fanout')
        for _ in range(self.config["rounds"]):
            dados = simula_dados_api()
            self.canal.basic_publish(exchange=self.config["exchange"], routing_key='',
                                     body=dados)
            print(f"[x] Enviando '{dados}'")

        self.conexao.close()


if __name__ == '__main__':
    mode = sys.argv[1].upper()
    print(f'MODE: {mode}')
    if mode == 'PUB_SUB':
        PubSub()
    elif mode == 'WORK_QUEUES':
        MensageriaSimples()
    else:
        MensageriaSimples()
