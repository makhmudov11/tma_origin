from datetime import timedelta

from django.db import models

from apps.users.models import Admin
from apps.utils.base import BaseCreateUpdateModel


class Answer(BaseCreateUpdateModel):
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
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'directory'

    def __str__(self):
        return self.name


class Archive(BaseCreateUpdateModel):
    user_image = models.CharField(max_length=100, null=True)
    user_full_name = models.CharField(max_length=255, null=True)
    user_email_address = models.CharField(max_length=255, blank=True, null=True, unique=True)
    user_type = models.CharField(max_length=50, null=True)
    collection_name = models.CharField(max_length=150)
    language = models.TextField(null=True, default='uz')
    collection_science_name = models.CharField(max_length=100)
    since_id = models.IntegerField(blank=True, null=True)
    max_attempts = models.IntegerField(default=1)
    givenminutes = models.DurationField(default=timedelta(minutes=1))
    amount_in_test = models.IntegerField()
    admin_image = models.CharField(max_length=100, null=True)
    admin_type = models.CharField(max_length=50, null=True)
    admin_full_name = models.CharField(max_length=255, null=True, db_index=True)
    admin_email_address = models.CharField(max_length=255, null=True, db_index=True, unique=True)
    directory_name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)
    faculty_name = models.CharField(max_length=145)
    stage = models.IntegerField(default=1)
    group_name = models.CharField(max_length=150)
    test_count = models.IntegerField()
    result = models.IntegerField()
    end_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)


class Meta:
    db_table = 'archive'


def __str__(self):
    return self.collection.name


class ArchiveAnswer(BaseCreateUpdateModel):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question_text = models.TextField()
    question_image = models.CharField(max_length=80, null=True)
    is_checked = models.BooleanField()
    collection_name = models.CharField(max_length=150)
    language = models.TextField(null=True, default='uz')
    collection_science_name = models.CharField(max_length=100)
    since_id = models.IntegerField(blank=True, null=True)
    directory_name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'archive_answer'

    def __str__(self):
        return self.text


class ArchiveQuestion(BaseCreateUpdateModel):
    text = models.CharField(max_length=255)
    collection_name = models.CharField(max_length=150)
    language = models.TextField(null=True, default='uz')
    collection_science_name = models.CharField(max_length=100)
    since_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'archive_question'

    def __str__(self):
        return self.text


class ArchiveCollection(BaseCreateUpdateModel):
    collection_name = models.CharField(max_length=150)
    language = models.TextField(null=True, default='uz')
    collection_science_name = models.CharField(max_length=100)
    since_id = models.IntegerField(blank=True, null=True)
    max_attempts = models.IntegerField(default=1)
    givenminutes = models.DurationField(default=timedelta(minutes=1))
    amount_in_test = models.IntegerField()
    admin_image = models.CharField(max_length=100, null=True)
    admin_type = models.CharField(max_length=50, null=True)
    admin_full_name = models.CharField(max_length=255, null=True, db_index=True)
    admin_email_address = models.CharField(max_length=255, null=True, db_index=True, unique=True)

    class Meta:
        db_table = 'archive_collection'
