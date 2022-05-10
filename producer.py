#!.venv/bin python
import os
import pika
from dotenv import load_dotenv
import random
import json
import sys


def DefinicaoEnv():
    load_dotenv()
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


def GeradorNomeCompleto():
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
    return str().join(random.sample(nome, 1) + random.sample(particula, 1) + random.sample(sobrenome, 1))


def SimulaDadosAPI():
    random.seed()
    api = [{
        "status": 200,
        "data": {
            "name": GeradorNomeCompleto(),
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
    return api


class MensageriaSimples:
    def __init__(self, *args, **kwargs):
        self.config = DefinicaoEnv()
        self.conexao = self.AbrirConexao()
        self.canal = self.conexao.channel()
        self.EnviaMensagem()

    def AbrirConexao(self):
        credenciais = pika.PlainCredentials(
            self.config["user"], self.config["passwd"])
        conexao = pika.BlockingConnection(pika.ConnectionParameters(
            self.config.server, self.config["port"], '/', credenciais))
        return conexao

    def EnviaMensagem(self):
        self.canal.queue_declare(queue=self.config["queue"])
        for _ in range(self.config["rounds"]):
            dados = SimulaDadosAPI()
            self.canal.basic_publish(exchange='', routing_key=self.config["queue"],
                                     body=json.dumps(dados))
            print(f"[x] Enviando '{dados}'")

        self.conexao.close()


if __name__ == '__main__':
    MensageriaSimples()
