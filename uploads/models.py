from django.db import models

class ProcessosPDF(models.Model):
    arquivo = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.arquivo.name

class ProcessInfo(models.Model):
    autor_nome = models.CharField(max_length=255, null=True, blank=True)
    autor_documento = models.CharField(max_length=20, null=True, blank=True)
    reus = models.JSONField(null=True, blank=True)  # Lista de nomes dos réus
    reus_documentos = models.JSONField(null=True, blank=True)  # Lista de documentos dos réus
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Processo do autor: {self.autor_nome}"
