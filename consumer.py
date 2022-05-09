#!.venv/bin python
import pika
import sys
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("RABBITMQ_USER")
passwd = os.getenv("RABBITMQ_PASS")
server = os.getenv("RABBITMQ_SERVER")
port = os.getenv("RABBITMQ_PORT")
queue = os.getenv("RABBITMQ_NAME_QUEUE")


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
