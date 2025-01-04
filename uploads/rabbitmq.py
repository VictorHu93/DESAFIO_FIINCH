import pika
import json

# Configuração do RabbitMQ
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'pdf_queue'

def get_rabbitmq_connection():
    """Estabelece a conexão com o RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    # Declara a fila caso ela não exista
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel

def send_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Garantir que a fila existe
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Enviar mensagem
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Tornar mensagem persistente
    )
    print(f"Mensagem enviada para a fila: {message}")
    connection.close()
