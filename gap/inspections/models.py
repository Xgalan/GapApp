from datetime import date

from django.db import models

from django_extensions.db.models import TimeStampedModel

from partnumbers.models import Partnumber



class Lot(TimeStampedModel):
    SUPPLIER = 'fn'
    SUBCONTRACTOR = 'tz'
    SCLPUN = 'sclpun'
    PRODUCTION = 'int_pr'
    TOROIDAL = 't'
    RELAY = 'r'
    MOLDING = 'QPS'
    TYPES_ = [
        (SUPPLIER, ''),
        (SUBCONTRACTOR, 'TZ'),
        (SCLPUN, 'SCL/pun'),
        (PRODUCTION, 'Produzione interna'),
        (TOROIDAL, 'T'),
        (RELAY, 'R'),
        (MOLDING, 'QPS')
    ]
    lot_number = models.IntegerField()
    lot_date = models.DateField(default=date.today)
    supplier_type = models.CharField(choices=TYPES_, max_length=6, default=SUPPLIER)
    partnumbers = models.ManyToManyField(Partnumber, through='pickings.Picking')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lot_number', 'lot_date', 'supplier_type'],
            name='unique_lot')
        ]
        ordering = ['-lot_date', 'lot_number']

    def __str__(self):
        s = "{self.lot_number} / {self.lot_date.year} ".format(self=self)
        s += self.get_supplier_type_display()
        return s
