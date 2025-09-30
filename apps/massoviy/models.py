from django.db import models

from apps.utils.base import BaseCreateUpdateModel

class PDFFile(BaseCreateUpdateModel):
    file = models.FileField(upload_to='file/question/')

    class Meta:
        db_table = 'pdffile'


class Question(BaseCreateUpdateModel):
    text = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to='qa/questions/', null=True)
    file = models.ForeignKey('PDFFile', on_delete=models.CASCADE, related_name='file_questions')

class Answer(BaseCreateUpdateModel):
    text = models.CharField(max_length=100, null=True)
    label = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='qa/answers/', null=True)
    question = models.ForeignKey('Question', models.CASCADE, related_name='question_answers')
    in_correct = models.BooleanField(default=False)
