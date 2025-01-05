import json
from django.conf import settings
from .rabbitmq import RabbitMQClient
from .models import ProcessosPDF, ProcessInfo
from utils.extract_pdf import extract_pdf_data


class PdfConsumer:
    @staticmethod
    def process_message(channel, method, properties, body):
        """
        Processa uma mensagem recebida da fila.
        """
        try:
            message = json.loads(body)
            pdf_id = message.get("id")

            # Buscar o PDF no banco
            pdf_instance = ProcessosPDF.objects.get(id=pdf_id)
            pdf_blob = pdf_instance.arquivo

            # Extrair dados do PDF
            extracted_data = extract_pdf_data(pdf_blob)

            # Persistir os dados extraídos
            ProcessInfo.create_from_extracted_data(extracted_data, pdf_instance)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag)

    @staticmethod
    def start_consuming():
        """
        Inicia o consumidor para processar mensagens da fila.
        """
        connection = RabbitMQClient.get_connection()
        channel = connection.channel()
        queue_name = settings.QUEUE_NAME

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(
            queue=queue_name, on_message_callback=PdfConsumer.process_message
        )
        print(f"Consumidor iniciado. Aguardando mensagens na fila...")
        channel.start_consuming()
