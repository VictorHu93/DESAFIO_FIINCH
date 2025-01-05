from django.urls import path
from .views import upload_pdfs, list_extracted_data

urlpatterns = [
    path("", upload_pdfs, name="upload_pdfs"),
    path("api/data/", list_extracted_data, name="list_extracted_data"),
]
