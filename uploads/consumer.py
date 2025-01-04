import pika
import json
import requests

# Configurações
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'pdf_queue'
API_URL = 'http://127.0.0.1:8000/uploads/api/extract/'

def callback(ch, method, properties, body):
    """Callback que processa cada mensagem da fila."""
    # Decodifica a mensagem JSON
    message = json.loads(body)
    file_path = message.get("file_path")

    print(f"Processando arquivo: {file_path}")

    try:
        # Lê o arquivo e envia para a API
        with open(file_path, 'rb') as file:
            response = requests.post(API_URL, files={'file': file})
            if response.status_code == 200:
                print(f"Sucesso: {response.json()}")
            else:
                print(f"Erro: {response.status_code}, {response.text}")

        # Confirma a mensagem como processada
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Erro ao processar: {e}")
        # Marca como não processada sem reencaminhamento
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    """Inicia o consumidor."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)  # Processa uma mensagem por vez
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("Aguardando mensagens. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
