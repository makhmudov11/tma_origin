import pdfplumber, re, os
from pdf2image import convert_from_path
import pytesseract
import magic
from PIL import Image
from rest_framework.generics import CreateAPIView

from apps.massoviy.models import PDFFile
from apps.massoviy.serializers import PDFFileSerializer
from cccccccccccc import parse_pdf


class PDFFileCreateAPIView(CreateAPIView):
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer

    def perform_create(self, serializer):
        file_obj = serializer.save()
        parse_pdf(file_obj.file.path, file_obj)
