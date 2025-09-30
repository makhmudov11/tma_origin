from django.urls import path

from apps.massoviy.views import PDFFileCreateAPIView

urlpatterns = [
    path('', PDFFileCreateAPIView.as_view())
]