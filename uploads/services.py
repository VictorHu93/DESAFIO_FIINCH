from .models import ProcessosPDF, ProcessInfo
from .rabbitmq import RabbitMQClient
from .models import ProcessInfo
from datetime import datetime
import os
import pandas as pd

class PdfService:
    @staticmethod
    def process_and_send_to_queue(arquivo):
        """
        Processa o arquivo PDF, salva no banco e envia à fila RabbitMQ.
        """
        # Salvar o arquivo no banco de dados
        try:
            processo = ProcessosPDF.objects.create(
                nome=arquivo.name,
                arquivo=arquivo.read(),  # Salva o conteúdo binário
            )
        except Exception as e:
            raise ValueError(f"Erro ao salvar no banco: {e}")

        # Criar mensagem para a fila
        message = {"id": processo.id, "nome": processo.nome}

        # Enviar mensagem para RabbitMQ
        try:
            RabbitMQClient.send_to_queue(message)
            print(f"Mensagem enviada para a fila: {message}")
        except Exception as e:
            raise ValueError(f"Erro ao enviar para a fila: {e}")
        
    @staticmethod
    def get_extracted_data():
        """
        Retorna dados extraídos armazenados no banco de dados.
        """
        return list(ProcessInfo.objects.all().values(
            "id",
            "autor_nome",
            "autor_documento",
            "reus",
            "reus_documentos",
            "criado_em",
        ))

    @staticmethod
    def get_queue_message_count():
        """
        Retorna a contagem de mensagens restantes na fila RabbitMQ.
        """
        return RabbitMQClient.get_message_count()
    
    @staticmethod
    def gerar_planilha(caminho_planilha):
        """
        Gera ou atualiza a planilha Excel com os dados dos processos.
        Retorna True se novos dados foram adicionados.
        """
        dados = list(ProcessInfo.objects.all().values(
            "numero_processo", "autor_nome", "autor_documento", "reus", "reus_documentos", "status", "criado_em"
        ))

        if not dados:
            return False  # Nenhum dado disponível para gerar a planilha

        df_novo = pd.DataFrame(dados)

        # Remover timezone de campos datetime
        if "criado_em" in df_novo.columns:
            df_novo["criado_em"] = df_novo["criado_em"].dt.tz_localize(None)

        if os.path.exists(caminho_planilha):
            # Comparar planilha existente com os novos dados
            df_existente = pd.read_excel(caminho_planilha)
            if df_novo.equals(df_existente):
                return False  # Nenhuma alteração nos dados

        # Salvar a nova planilha
        df_novo.to_excel(caminho_planilha, index=False)
        return True