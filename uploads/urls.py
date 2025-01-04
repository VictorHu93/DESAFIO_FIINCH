from django.urls import path
from .views import upload_pdfs, extract_pdf_info, list_extracted_data

urlpatterns = [
    path('', upload_pdfs, name='upload_pdfs'), 
    path('api/extract/', extract_pdf_info, name='extract_pdf_info'),
    path('api/data/', list_extracted_data, name='list_extracted_data'),
    
]
