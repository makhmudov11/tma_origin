import magic
from rest_framework import serializers

from apps.massoviy.models import PDFFile


class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['file']

    @staticmethod
    def is_pdf(file_obj):
        mime = magic.from_buffer(file_obj.read(2048), mime=True)
        file_obj.seek(0)
        return mime == "application/pdf"

    def validate_file(self, file_obj):
        if not self.is_pdf(file_obj):
            raise serializers.ValidationError("Faqat PDF fayl yuklash mumkin!")
        return file_obj
