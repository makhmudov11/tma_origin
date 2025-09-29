from django.db import models

from apps.utils.base import BaseCreateUpdateModel


class Setting(BaseCreateUpdateModel):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    status = models.BooleanField()

    class Meta:
        db_table = 'setting'
