#!.venv/bin python
import os
import pika
from dotenv import load_dotenv
import random
import json

load_dotenv()
user = os.getenv("RABBITMQ_USER")
passwd = os.getenv("RABBITMQ_PASS")
server = os.getenv("RABBITMQ_SERVER")
port = os.getenv("RABBITMQ_PORT")
queue = os.getenv("RABBITMQ_NAME_QUEUE")
rounds = int(os.getenv("MAX_RUNS"))


credenciais = pika.PlainCredentials(user, passwd)
connection = pika.BlockingConnection(
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
for i in range(rounds):

    random.seed()
    api = [
        {"status": 200,
         "data": {
             "name": "Abel Menezes",
             "valor": random.sample(range(100), 1),
             "parcelas": random.sample(range(10), 1)
         }
         },
    ]
    # print(f"[x] {item}")
    channel.basic_publish(exchange='', routing_key=queue,
                          body=json.dumps(api))
    print(f"[x] Enviando '{api}'")

connection.close()
