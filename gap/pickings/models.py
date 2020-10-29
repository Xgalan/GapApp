import uuid

from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel

from partnumbers.models import Partnumber
from inspections.models import Lot



class Picking(TimeStampedModel):
    partnumber = models.ForeignKey(Partnumber, on_delete=models.RESTRICT)
    lot = models.ForeignKey(Lot, on_delete=models.RESTRICT)
    picking_operator = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT)
    picking_date = models.DateField()

    def __str__(self):
        return "{self.partnumber} | {self.lot} | {self.picking_date}".format(self=self)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('picking_update', args=[str(self.id)])
