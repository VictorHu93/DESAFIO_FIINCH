from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadsViewsTestCase(TestCase):
    def setUp(self):
        # Configurar o cliente de teste
        self.client = Client()

        # Endpoints das rotas
        self.upload_url = reverse('upload_pdfs')
        self.list_data_url = reverse('list_extracted_data')

    def test_upload_pdfs_view_get(self):
        """Teste para verificar se a view de upload responde corretamente ao GET."""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uploads/upload_pdfs.html')  # Altere para o nome correto do template

    def test_upload_pdfs_view_post(self):
        """Teste para verificar o upload de arquivos via POST."""
        file_data = SimpleUploadedFile(
            "test.pdf", b"%PDF-1.4 test content", content_type="application/pdf"
        )
        response = self.client.post(self.upload_url, {"file": file_data})
        self.assertEqual(response.status_code, 200)
        # Você pode validar a lógica do que deve acontecer após o upload aqui

    def test_list_extracted_data_view(self):
        """Teste para verificar se a API de listar dados retorna corretamente."""
        response = self.client.get(self.list_data_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")  # Supondo que retorna JSON
        # Verifique o conteúdo retornado se necessário:
        # self.assertContains(response, "expected_data")
