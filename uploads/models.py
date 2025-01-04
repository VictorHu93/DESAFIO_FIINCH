from django.db import models

class ProcessosPDF(models.Model):
    """
    Modelo para armazenar arquivos PDF de processos jurídicos.
    """
    nome = models.CharField(max_length=255, null=False)  # Nome do arquivo
    arquivo = models.BinaryField()  # Blob para armazenar o PDF
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.upload_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def save_pdf(self, arquivo):
        """
        Salva um arquivo PDF no banco de dados.
        """
        self.arquivo = arquivo.read()
        self.save()


class ProcessInfo(models.Model):
    """
    Modelo para armazenar informações extraídas de um processo.
    """
    STATUS_EM_ANDAMENTO = 'Em Andamento'
    STATUS_FINALIZADO = 'Finalizado'

    STATUS_CHOICES = [
        (STATUS_EM_ANDAMENTO, 'Em Andamento'),
        (STATUS_FINALIZADO, 'Finalizado'),
    ]

    numero_processo = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número do Processo")
    autor_nome = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome do Autor")
    autor_documento = models.CharField(max_length=20, null=True, blank=True, verbose_name="Documento do Autor")
    reus = models.JSONField(null=True, blank=True, verbose_name="Réus (Nomes)")  # Lista de nomes dos réus
    reus_documentos = models.JSONField(null=True, blank=True, verbose_name="Réus (Documentos)")  # Lista de documentos dos réus
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_EM_ANDAMENTO,
        verbose_name="Status do Processo"
    )
    pdf = models.ForeignKey(ProcessosPDF, on_delete=models.CASCADE, related_name="processos_info")

    def __str__(self):
        return f"Processo {self.numero_processo or 'Desconhecido'} - {self.status} - {self.autor_nome or 'Autor Desconhecido'}"

    @classmethod
    def create_from_extracted_data(cls, extracted_data, pdf_instance):
        """
        Cria um registro de informações do processo com base nos dados extraídos.
        """
        return cls.objects.create(
            numero_processo=extracted_data.get("processo_numero"),
            status=extracted_data.get("status"),
            autor_nome=extracted_data.get("autor_nome"),
            autor_documento=extracted_data.get("autor_documento"),
            reus=[r.get("nome") for r in extracted_data.get("reus", [])],
            reus_documentos=[r.get("documento") for r in extracted_data.get("reus", [])],
            pdf=pdf_instance,
        )
