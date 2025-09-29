from datetime import timedelta

from django.db import models

from apps.users.models import Admin
from apps.utils.base import BaseCreateUpdateModel


class Answer(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='qa/answers/', null=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('qa.Question', models.SET_NULL, null=True, related_name='question_answers')

    class Meta:
        db_table = 'answer'
        verbose_name = 'answer'
        verbose_name_plural = 'answers'
        ordering = ['-id']

    def __str__(self):
        return self.text or self.id


class Question(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    text = models.TextField()
    image = models.ImageField(upload_to='qa/questions/', null=True)
    collection = models.ForeignKey('qa.Collection', models.SET_NULL, null=True, related_name='collection_questions')
    # image_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'question'
        verbose_name = 'question'
        verbose_name_plural = 'questions'

    def __str__(self):
        return self.text


class Collection(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=150)
    language = models.TextField(null=True, default='uz')
    science = models.ForeignKey('department.Science', models.SET_NULL, null=True, related_name='science_collections')
    max_attempts = models.IntegerField(default=1)
    givenminutes = models.DurationField(default=timedelta(minutes=1))
    amount_in_test = models.IntegerField()
    admin = models.ForeignKey(Admin, models.SET_NULL, blank=True, null=True, related_name='admin_collections')
    directory = models.ForeignKey('qa.Directory', models.SET_NULL,
                                  blank=True, null=True, related_name='directory_collections')

    class Meta:
        db_table = 'collection'
        ordering = ['name']

    def __str__(self):
        return self.name



class Directory(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'directory'

    def __str__(self):
        return self.name


class Archive(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='archives_user')
    collection = models.ForeignKey('qa.Collection', on_delete=models.SET_NULL,
                                   null=True, related_name='collection_archives')
    faculty = models.ForeignKey('department.Faculty', on_delete=models.SET_NULL, null=True, related_name='faculty_archives')
    course = models.ForeignKey('department.Course', on_delete=models.SET_NULL, null=True, related_name='course_archives')
    group = models.ForeignKey('department.Group', on_delete=models.SET_NULL, null=True, related_name='group_archives')
    test_count = models.IntegerField()
    result = models.IntegerField()
    end_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'archive'


    def __str__(self):
        return self.collection.name



class ArchiveAnswer(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('qa.ArchiveQuestion', on_delete=models.SET_NULL,
                                 null=True, related_name='archive_question_archives')
    is_checked = models.BooleanField()

    class Meta:
        db_table = 'archive_answer'

    def __str__(self):
        return self.text

class ArchiveQuestion(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    collection = models.ForeignKey('qa.ArchiveCollection', on_delete=models.SET_NULL,
                                   null=True, related_name='archive_collection_questions')

    class Meta:
        db_table = 'archive_question'

    def __str__(self):
        return self.text



class ArchiveCollection(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(Admin, models.DO_NOTHING, blank=True, null=True)
    language = models.TextField(default='uz')
    science = models.ForeignKey('department.Science', on_delete=models.SET_NULL,
                                null=True, related_name='science_archive_collections')
    archive = models.OneToOneField(Archive, on_delete=models.SET_NULL, null=True,
                                   related_name='archive_archive_collections')
    max_attempts = models.IntegerField()
    givenminutes = models.DurationField(default=timedelta(minutes=1))
    amount_in_test = models.IntegerField()

    class Meta:
        db_table = 'archive_collection'


