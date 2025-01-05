from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("uploads/", include("uploads.urls")),  # Inclui as rotas do app 'uploads'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
