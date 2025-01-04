from django.shortcuts import render, redirect
from django.contrib import messages
from .services import PdfService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

def upload_pdfs(request):
    """
    Faz o upload de PDFs e gera a planilha atualizada, se necessário.
    """
    if request.method == "POST":
        arquivos = request.FILES.getlist("arquivo")

        if not arquivos:
            return JsonResponse({"success": False, "message": "Nenhum arquivo selecionado para envio."})

        for arquivo in arquivos:
            PdfService.process_and_send_to_queue(arquivo)

        # Gerar ou atualizar a planilha
        caminho_planilha = "data/dados_processados.xlsx"
        planilha_atualizada = PdfService.gerar_planilha(caminho_planilha)

        # Retornar para o frontend o status da planilha
        return JsonResponse({
            "success": True,
            "planilha_atualizada": planilha_atualizada,
            "message": "Arquivos enviados com sucesso!",
        })

    return render(request, "uploads/upload_pdfs.html")


@api_view(["GET"])
def list_extracted_data(request):
    """
    Lista os dados extraídos do banco de dados e mensagens restantes na fila.
    """
    try:
        extracted_data = PdfService.get_extracted_data()
        remaining_in_queue = PdfService.get_queue_message_count()
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({
        "extracted_data": extracted_data,
        "remaining_in_queue": remaining_in_queue,
    }, status=200)
