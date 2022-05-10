#!.venv/bin python
import pika
import sys
import os
from dotenv import load_dotenv
import time


def DefinicaoEnv():
load_dotenv()
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
    def __init__(self, *args, **kwargs):
        self.config = DefinicaoEnv()
        self.conexao = self.AbrirConexao()
        self.canal = self.conexao.channel()
        self.RecebeMensagem()

    def AbrirConexao(self):
        credenciais = pika.PlainCredentials(
            self.config["user"], self.config["passwd"])
        conexao = pika.BlockingConnection(pika.ConnectionParameters(
            self.config["server"], self.config["port"], '/', credenciais))
        return conexao

    def RecebeMensagem(self):
        self.canal.queue_declare(queue=self.config["queue"])

        def callback(ch, method, properties, body):
            print(f" [x] Opa recebi a mensagem {body}")

        self.canal.basic_consume(
            queue=self.config["queue"], on_message_callback=callback, auto_ack=True)

        print(' [*] Esperando por mensagens. CTRL+C para sair')
        self.canal.start_consuming()


class WorkQueues:
    def __init__(self, *args, **kwargs):
        self.config = DefinicaoEnv()
        self.conexao = self.AbrirConexao()
        self.canal = self.conexao.channel()
        self.RecebeMensagem()

    def AbrirConexao(self):
        credenciais = pika.PlainCredentials(
            self.config["user"], self.config["passwd"])
        conexao = pika.BlockingConnection(pika.ConnectionParameters(
            self.config["server"], self.config["port"], '/', credenciais))
        return conexao

    def RecebeMensagem(self):
        self.canal.queue_declare(queue=self.config["queue"])

        def callback(ch, method, properties, body):
            print(f" [x] Opa recebi a mensagem {body}")
            time.sleep(body.count(b'.'))
            print(" [x] Feito meu chapa!")
            self.canal.basic_ack(delivery_tag=method.delivery_tag)

        self.canal.basic_consume(
            queue=self.config["queue"], on_message_callback=callback)

        print(' [*] Esperando por mensagens. CTRL+C para sair')
        self.canal.start_consuming()


class PubSub:
    def __init__(self, *args, **kwargs):
        self.config = DefinicaoEnv()
        self.conexao = self.AbrirConexao()
        self.canal = self.conexao.channel()
        self.RecebeMensagem()

crdentials = pika.PlainCredentials(user, passwd)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(server, port, '/', crdentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        print(f" [x] Opa recebi a mensagem {body}")

    channel.basic_consume(
        queue=queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando por mensagens. CTRL+C para sair')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
