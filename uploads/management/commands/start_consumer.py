from django.core.management.base import BaseCommand
from uploads.consumer import PdfConsumer


class Command(BaseCommand):
    help = "Inicia o consumidor RabbitMQ para processar PDFs."

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o consumidor RabbitMQ...")
        try:
            # Instanciando o consumidor
            consumer = PdfConsumer()
            consumer.start_consuming()
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING("\nConsumo interrompido pelo usuário.")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro durante o consumo: {e}"))
