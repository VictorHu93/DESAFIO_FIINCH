from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import PdfService, PlanilhaService, FilaService
from rest_framework.pagination import PageNumberPagination


def upload_pdfs(request):
    """
    Faz o upload de PDFs, envia para a fila e cria uma planilha diária.
    """
    if request.method == "POST":
        arquivos = request.FILES.getlist("arquivo")

        if not arquivos:
            return JsonResponse(
                {"success": False, "message": "Nenhum arquivo selecionado para envio."}
            )

        try:
            for arquivo in arquivos:
                PdfService.process_and_send_to_queue(arquivo)

            # Gerar planilha do dia
            planilha_criada = PlanilhaService.gerar_planilha_por_dia()
            return JsonResponse(
                {
                    "success": True,
                    "planilha_criada": planilha_criada,
                    "message": "Arquivos enviados e planilha diária criada!",
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, "uploads/upload_pdfs.html")


@api_view(["GET"])
def list_extracted_data(request):
    """
    Lista os dados extraídos do banco de dados com paginação.
    """
    try:
        extracted_data = PdfService.get_extracted_data()
        remaining_in_queue = FilaService.get_queue_message_count()

        # Configuração de paginação
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Define o número de itens por página
        paginated_data = paginator.paginate_queryset(extracted_data, request)

        return paginator.get_paginated_response({
            "extracted_data": paginated_data,
            "remaining_in_queue": remaining_in_queue,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
