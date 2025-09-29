from django.db import models

from apps.utils.base import BaseCreateUpdateModel
from apps.utils.other_model import *


class Admin(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    image = models.ImageField(upload_to='users/', null=True)
    type = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, db_index=True)
    email_address = models.CharField(max_length=255, null=True, db_index=True, unique=True)

    class Meta:
        db_table = 'admin'
        verbose_name = 'admin'
        verbose_name_plural = 'admins'
        ordering = ['-id']

    def __str__(self):
        return self.full_name or self.email_address or self.id



class User(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    image = models.ImageField(upload_to='users/', null=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True, unique=True)
    type = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'user'
        ordering = ['-id']

    def __str__(self):
        return self.full_name or self.email_address or self.id


class UserCollection(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collection_user')
    have_attempt = models.IntegerField()
    collection = models.ForeignKey('qa.Collection', on_delete=models.SET_NULL, null=True, related_name='user_collection')

    class Meta:
        db_table = 'user_collection'

    def __str__(self):
        return self.id



class UserInfo(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='user_info')
    hemis_id = models.CharField(max_length=255)
    group = models.ForeignKey('department.Group', on_delete=models.SET_NULL, null=True, related_name='group_user_info')


    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return self.id


class UserLog(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    hemis_id = models.CharField(max_length=128)
    fullname = models.CharField(max_length=64)
    group = models.ForeignKey('department.Group', on_delete=models.SET_NULL, null=True, related_name='group_user_log')
    course = models.SmallIntegerField()
    group_name = models.CharField(max_length=128)
    faculty = models.CharField(max_length=255)


    class Meta:
        db_table = 'user_log'

    def __str__(self):
        return self.hemis_id



class UserResult(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    collection_id = models.UUIDField()
    hemis_id = models.CharField(max_length=64)
    compyuter_name = models.CharField(max_length=255)
    collection_name = models.CharField(max_length=255, blank=True, null=True)
    grade = models.IntegerField()
    user_fullname = models.CharField(max_length=255, null=True)
    group_name = models.CharField(max_length=255, null=True)
    faculty_name = models.CharField(max_length=255)
    course = models.SmallIntegerField()
    all_question_count = models.SmallIntegerField()
    find_question_count = models.SmallIntegerField()
    has_finished = models.BooleanField()
    is_pending = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    until_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_result'


class UserResultAnswerData(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    user_result = models.ForeignKey(UserResult, on_delete=models.SET_NULL,
                                    null=True, related_name='user_result_answer_data')
    question_name = models.CharField(max_length=255, blank=True, null=True)
    question_image_url = models.CharField(max_length=255, blank=True, null=True)
    correct_answer_count = models.IntegerField()
    find_answer_count = models.IntegerField()
    question_number = models.IntegerField()
    get_time = models.CharField(max_length=10)

    class Meta:
        db_table = 'user_result_answer_data'

    def __str__(self):
        return self.id