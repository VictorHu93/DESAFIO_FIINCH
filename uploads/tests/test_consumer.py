import json
from unittest.mock import patch, MagicMock
from django.test import TestCase
from uploads.models import ProcessosPDF, ProcessInfo
from uploads.consumer import PdfConsumer


class PdfConsumerTestCase(TestCase):
    def setUp(self):
        self.pdf = ProcessosPDF.objects.create(
            nome="arquivo_teste.pdf",
            arquivo=b"conteudo_em_binario"
        )

    @patch("uploads.models.ProcessosPDF.objects.get")
    @patch("uploads.consumer.extract_pdf_data")
    def test_process_message(self, mock_extract, mock_get):
        """
        Testa o processamento de uma mensagem pela fila.
        """
        mock_get.return_value = self.pdf
        mock_extract.return_value = {
            "processo_numero": "12345",
            "status": "Em Andamento",
            "autor_nome": "Autor Teste",
            "autor_documento": "123.456.789-00",
            "reus": [{"nome": "Réu 1", "documento": "987.654.321-00"}]
        }

        # Mock para o channel e o method
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_method.delivery_tag = 12345

        # Simula o processamento da mensagem
        PdfConsumer.process_message(
            mock_channel, mock_method, None, json.dumps({"id": self.pdf.id}).encode()
        )

        # Verifica se o registro foi criado no banco de dados
        process_info_exists = ProcessInfo.objects.filter(numero_processo="12345").exists()
        self.assertTrue(process_info_exists)

        # Verifica se o método basic_ack foi chamado
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=12345)
