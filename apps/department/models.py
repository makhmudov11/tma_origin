from django.db import models

from apps.utils.base import BaseCreateUpdateModel


class Science(BaseCreateUpdateModel):
    name = models.CharField(max_length=100)
    since_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'science'
        ordering = ['-since_id']

    def __str__(self):
        return self.name or self.since_id


class Course(BaseCreateUpdateModel):
    stage = models.IntegerField(default=1)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.stage


class Faculty(BaseCreateUpdateModel):
    name = models.CharField(max_length=145)

    class Meta:
        db_table = 'faculty'

    def __str__(self):
        return self.name


class Group(BaseCreateUpdateModel):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, models.SET_NULL, null=True, related_name='course_groups')
    faculty = models.ForeignKey(Faculty, models.SET_NULL, null=True, related_name='faculty_groups')

    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.name
