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
    lot_number = models.IntegerField(
        verbose_name='nr. lotto'
    )
    lot_date = models.DateField(
        default=date.today,
        verbose_name='data di consegna'
    )
    supplier_type = models.CharField(
        choices=TYPES_, max_length=6, default=SUPPLIER,
        verbose_name='tipo di fornitura'
    )
    partnumbers = models.ManyToManyField(Partnumber, through='pickings.Picking')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lot_number', 'lot_date', 'supplier_type'],
            name='unique_lot')
        ]
        ordering = ['-lot_date', 'lot_number']
        verbose_name='lotto'

    def __str__(self):
        d = self.get_supplier_type_display()
        lot_year = self.lot_date.strftime("%y")
        lot_date = self.lot_date.strftime("%d/%m/%Y")
        std = "{self.lot_number} / {lot_year}".format(self=self, lot_year=lot_year)
        case = {
            'fn': std + d,
            'tz': std + d,
            'sclpun': d + " {lot_date}".format(lot_date=lot_date),
            'int_pr': d,
            't': std + d,
            'r': std + d,
            'QPS': d + ' ' + std,
        }
        return case[self.supplier_type]
