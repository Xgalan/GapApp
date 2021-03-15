from django.db import models

from treebeard.mp_tree import MP_Node

from partnumbers.models import Partnumber

from django_extensions.db.models import TimeStampedModel



class Item(TimeStampedModel):
    PICKING = 'pg'
    STORAGE = 'se'
    AREA = [
        (PICKING, 'Area prelievo'),
        (STORAGE, 'Area magazzino')
    ]
    partnumber = models.ForeignKey(
        Partnumber, on_delete=models.RESTRICT, verbose_name='codice'
    )
    storage = models.ForeignKey(
        'Storage', on_delete=models.RESTRICT, verbose_name='magazzino'
    )
    area = models.CharField(
        max_length=3,
        choices=AREA,
        default=PICKING,
        verbose_name='destinazione'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['partnumber', 'storage'], name='unique_partnumber_storage')
        ]

    def __str__(self):
        area = self.get_area_display()
        return "{self.partnumber} | {self.storage} | ".format(self=self) + area


class Storage(MP_Node):
    SHELF = 'sh'
    SECTION = 'se'
    SHELVING_UNIT = 'shu'
    DRAWER_UNIT = 'dru'
    DRAWER = 'dr'
    AREA = 'ar'
    BIN = 'bin'
    TYPES_ = [
        (SHELF, 'Ripiano'),
        (SECTION, 'Sezione'),
        (SHELVING_UNIT, 'Scaffalatura'),
        (DRAWER_UNIT, 'Cassettiera'),
        (DRAWER, 'Cassetto'),
        (AREA, 'Area'),
        (BIN, 'Contenitore')
    ]
    location = models.CharField(
        verbose_name='coordinata',
        max_length=30
    )
    container_type = models.CharField(
        max_length=3,
        choices=TYPES_,
        default=SHELF,
        verbose_name='tipo di contenitore'
    )
    items = models.ManyToManyField(
        Partnumber, 
        through='warehouse.Item'
    )
    node_order_by = ['location']

    def __str__(self):
        container_type = self.get_container_type_display()
        return container_type + ': {self.location}'.format(self=self)