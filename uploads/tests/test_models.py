from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from uploads.models import ProcessosPDF, ProcessInfo


class ProcessosPDFTestCase(TestCase):
    def test_processos_pdf_creation(self):
        """
        Testa a criação de um ProcessosPDF.
        """
        pdf_file = SimpleUploadedFile("arquivo_teste.pdf", b"conteudo_em_binario")
        pdf = ProcessosPDF.objects.create(
            nome=pdf_file.name,
            arquivo=pdf_file.read()
        )
        self.assertEqual(pdf.nome, "arquivo_teste.pdf")
        self.assertIsNotNone(pdf.upload_date)


class ProcessInfoTestCase(TestCase):
    def setUp(self):
        pdf_file = SimpleUploadedFile("arquivo_teste.pdf", b"conteudo_em_binario")
        self.pdf = ProcessosPDF.objects.create(
            nome=pdf_file.name,
            arquivo=pdf_file.read()
        )

    def test_process_info_creation(self):
        """
        Testa a criação de informações de processo (ProcessInfo).
        """
        process_info = ProcessInfo.objects.create(
            numero_processo="12345",
            autor_nome="Autor Teste",
            autor_documento="123.456.789-00",
            reus=[{"nome": "Réu 1"}, {"nome": "Réu 2"}],
            reus_documentos=["987.654.321-00", "111.222.333-44"],
            pdf=self.pdf
        )
        self.assertEqual(process_info.numero_processo, "12345")
        self.assertEqual(process_info.autor_nome, "Autor Teste")
        self.assertEqual(process_info.reus[0]["nome"], "Réu 1")
        self.assertEqual(process_info.pdf, self.pdf)
