from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProcessosPDF, ProcessInfo
from .rabbitmq import send_to_queue
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PyPDF2 import PdfReader
import re


def upload_pdfs(request):
    if request.method == 'POST':
        arquivos = request.FILES.getlist('arquivo')

        if not arquivos:
            messages.error(request, "Nenhum arquivo selecionado para envio.")
        elif len(arquivos) > 5:
            messages.error(request, "Você só pode enviar até 5 arquivos por vez.")
        else:
            for arquivo in arquivos:
                # Salva cada arquivo no modelo ProcessosPDF
                processo = ProcessosPDF.objects.create(arquivo=arquivo)

                # Envia para a fila RabbitMQ
                message = {
                    "id": processo.id,
                    "file_name": processo.arquivo.name,
                    "file_path": processo.arquivo.path,
                }
                send_to_queue(message)

            messages.success(request, "Arquivos enviados com sucesso e adicionados à fila!")
            return redirect('upload_pdfs')

    return render(request, 'uploads/upload_pdfs.html')

@api_view(['POST'])
def extract_pdf_info(request):
    if 'file' not in request.FILES:
        return Response({"error": "Nenhum arquivo enviado"}, status=400)

    pdf_file = request.FILES['file']
    try:
        # Leitura do texto do PDF
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Extração do autor
        autor_nome_match = re.search(r"Autor:\s*([^\n]+)", text)
        autor_nome = autor_nome_match.group(1).split("Documento Autor:")[0].strip() if autor_nome_match else None

        autor_doc_match = re.search(r"Documento Autor:\s*([\d\.\-]+)", text)
        autor_doc = autor_doc_match.group(1).strip() if autor_doc_match else None

        # Extração dos réus e documentos
        reus_matches = re.findall(r"Réu:\s*([^:\n]+)\s*Documento Réu:\s*([\d\.\-]+)", text)
        reus = [{"nome": match[0].strip(), "documento": match[1].strip()} for match in reus_matches]

        # Salvar no banco de dados
        process_info = ProcessInfo.objects.create(
            autor_nome=autor_nome,
            autor_documento=autor_doc,
            reus=[r["nome"] for r in reus],
            reus_documentos=[r["documento"] for r in reus],
        )

        # Retornar os dados no formato refinado
        data = {
            "id": process_info.id,
            "autor": {
                "nome": autor_nome,
                "documento": autor_doc,
            },
            "reus": reus,
            "criado_em": process_info.criado_em,
        }
        return Response(data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def list_extracted_data(request):
    processos = ProcessInfo.objects.all()
    data = []
    for processo in processos:
        data.append({
            "id": processo.id,
            "autor": {
                "nome": processo.autor_nome,
                "documento": processo.autor_documento,
            },
            "reus": [
                {"nome": nome, "documento": doc}
                for nome, doc in zip(processo.reus, processo.reus_documentos)
            ],
            "criado_em": processo.criado_em,
        })
    return Response(data, status=200)
