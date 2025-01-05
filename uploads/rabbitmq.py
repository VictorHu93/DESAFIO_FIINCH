from django.conf import settings
import pika
import json


class RabbitMQClient:
    @staticmethod
    def get_connection():
        """
        Estabelece conexão com RabbitMQ.
        """
        try:
            rabbitmq_host = settings.RABBITMQ_HOST
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host)
            )
        except Exception as e:
            raise ValueError(f"Erro ao conectar ao RabbitMQ: {e}")

    @staticmethod
    def send_to_queue(message):
        """
        Envia uma mensagem à fila RabbitMQ.
        """
        try:
            queue_name = settings.QUEUE_NAME
            connection = RabbitMQClient.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            connection.close()
        except Exception as e:
            raise ValueError(f"Erro ao enviar mensagem para a fila: {e}")

    @staticmethod
    def get_message_count():
        """
        Obtém a contagem de mensagens restantes na fila RabbitMQ.
        """
        try:
            queue_name = settings.QUEUE_NAME
            connection = RabbitMQClient.get_connection()
            channel = connection.channel()
            queue_status = channel.queue_declare(queue=queue_name, passive=True)
            message_count = queue_status.method.message_count
            connection.close()
            return message_count
        except Exception as e:
            raise ValueError(f"Erro ao obter contagem de mensagens: {e}")
