#!.venv/bin python
"""
Código que implementa um consumidor de mensagens do RabbitMQ

### Clases
 - MensageriaSimples: Padrão de consumo simples por um canal e fila
 - WorkQueues: Padrão de consumo Work Queues
 - PubSub: Padrão de consumo Publisher/Subscriber
"""
import os
import sys
import time
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
    }
    return config


class MensageriaSimples:
    """
    ## Mensageria Simples

    Classe que implementa a troca de mensagens com o RabbitMQ
    atraves de uma canal e uma fila pré estabelicida

    #### Métodos

    - abrir_conexao(self)
    - recebe_mensagem(self)
    """

    def __init__(self):
        self.config = definicao_env()
        self.conexao = self.abrir_conexao()
        self.canal = self.conexao.channel()
        self.recebe_mensagem()

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

    def recebe_mensagem(self):
        """
        Método de receptação de mensagens do RabbitMQ pelo canal e fila
        """
        self.canal.queue_declare(queue=self.config["queue"])

        def callback(canal, metodo, propriedade, corpo):
            print(f" [x] Opa uma mensagem em: {canal}")
            print(f" ---[x] Com o método {metodo} e propriedade {propriedade}")
            print(f" ---[xx] Mensagem {corpo}")

        self.canal.basic_consume(
            queue=self.config["queue"], on_message_callback=callback, auto_ack=True)

        print(' [*] Esperando por mensagens. CTRL+C para sair')
        self.canal.start_consuming()


class WorkQueues:
    """
    ## Work Queues

    Classe que implementa a troca de mensagens com o RabbitMQ
    com o padrão Work Queues onde você tem 1 ou mais consumidores

    #### Métodos

    - abrir_conexao(self)
    - recebe_mensagem(self)
    """

    def __init__(self):
        self.config = definicao_env()
        self.conexao = self.abrir_conexao()
        self.canal = self.conexao.channel()
        self.recebe_mensagem()

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

    def recebe_mensagem(self):
        """
        Método de receptação de mensagens do RabbitMQ pelo canal e fila
        """
        self.canal.queue_declare(queue=self.config["queue"])

        def callback(canal, metodo, propriedade, corpo):
            print(f" [x] Opa uma mensagem em: {canal}")
            print(f" ---[x] Com o método {metodo} e propriedade {propriedade}")
            print(f" ---[xx] Mensagem {corpo}")
            # Simulo algum processamento
            time.sleep(corpo.count(b'.'))
            print(" [x] Feito meu chapa!")
            self.canal.basic_ack(delivery_tag=metodo.delivery_tag)

        self.canal.basic_consume(
            queue=self.config["queue"], on_message_callback=callback)

        print(' [*] Esperando por mensagens. CTRL+C para sair')
        self.canal.start_consuming()


class PubSub:
    """
    ## Publish/Subscribe

    Classe que implementa a troca de mensagens com o RabbitMQ
    no padrão Pub/Sub onde as mansegens são enfileiradas para varios consumidores
    atraves da exchange

    #### Métodos

    - abrir_conexao(self)
    - recebe_mensagem(self)
    """

    def __init__(self):
        self.config = definicao_env()
        self.conexao = self.abrir_conexao()
        self.canal = self.conexao.channel()
        self.recebe_mensagem()

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

    def recebe_mensagem(self):
        """
        Método de receptação de mensagens do RabbitMQ pela exchange
        """
        self.canal.exchange_declare(
            exchange=self.config["exchange"], exchange_type='fanout')

        queue_local = self.canal.queue_declare(
            queue='', exclusive=True).method.queue

        self.canal.queue_bind(
            exchange=self.config["exchange"], queue=queue_local)

        def callback(canal, metodo, propriedade, corpo):
            print(f" [x] Opa uma mensagem em: {canal}")
            print(f" ---[x] Com o método {metodo} e propriedade {propriedade}")
            print(f" ---[xx] Mensagem {corpo}")

        self.canal.basic_consume(
            queue=queue_local, on_message_callback=callback, auto_ack=True)

        print(' [*] Esperando por mensagens. CTRL+C para sair')
        self.canal.start_consuming()


def main():
    """
    Função principal do código
    """
    mode = sys.argv[1].upper()
    print(f'MODE: {mode}')
    if mode == 'PUB_SUB':
        PubSub()
    elif mode == 'WORK_QUEUES':
        WorkQueues()
    else:
        MensageriaSimples()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
