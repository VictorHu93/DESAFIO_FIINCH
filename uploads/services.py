from .models import ProcessosPDF, ProcessInfo
from .rabbitmq import RabbitMQClient
import pandas as pd
from datetime import date


class PdfService:
    @staticmethod
    def process_and_send_to_queue(arquivo):
        """
        Processa o arquivo PDF, salva no banco e envia à fila RabbitMQ.
        """
        processo = ProcessosPDF.objects.create(
            nome=arquivo.name,
            arquivo=arquivo.read(),
        )
        message = {"id": processo.id, "nome": processo.nome}
        RabbitMQClient.send_to_queue(message)

    @staticmethod
    def get_extracted_data():
        """
        Retorna dados extraídos armazenados no banco de dados.
        """
        return list(
            ProcessInfo.objects.all().values(
                "id",
                "numero_processo",
                "autor_nome",
                "autor_documento",
                "reus",
                "reus_documentos",
                "status",
                "criado_em",
            )
        )


class PlanilhaService:
    @staticmethod
    def gerar_planilha_por_dia():
        """
        Gera uma planilha para os processos do dia.
        """
        data_hoje = date.today().strftime("%Y-%m-%d")
        caminho_planilha = f"data/{data_hoje}_processos.xlsx"

        dados = list(
            ProcessInfo.objects.filter(criado_em__date=data_hoje).values(
                "numero_processo",
                "autor_nome",
                "autor_documento",
                "reus",
                "reus_documentos",
                "status",
            )
        )

        if not dados:
            return False

        df = pd.DataFrame(dados)
        df.to_excel(caminho_planilha, index=False)
        return True


class FilaService:
    @staticmethod
    def get_queue_message_count():
        """
        Retorna a contagem de mensagens restantes na fila RabbitMQ.
        """
        return RabbitMQClient.get_message_count()
