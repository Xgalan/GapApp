from django.db import models
from django.core.serializers import json

from django_extensions.db.models import TimeStampedModel

from core.mixins import SourceType


class Source(TimeStampedModel):
    shortform = models.CharField(
        choices=SourceType.choices,
        default=SourceType.SUPPLIER,
        max_length=6,
        unique=True,
    )
    description = models.CharField(max_length=60, unique=True, db_index=True)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return "{self.shortform} | {self.description}".format(self=self)
