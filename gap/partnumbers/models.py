import uuid
from operator import iconcat

from django.db import models

from django_extensions.db.models import TimeStampedModel



class Category(TimeStampedModel):
    category_name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ('category_name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return "%s" % self.category_name


class DbManager(models.Manager):
    """
    Utilities that returns data relatives to weight scale database
    """
    def get_max_nr(self):
        # Find the MAX db_nr
        return self.aggregate(models.Max('db_nr'))

    def new_db_nr(self):
        q = self.get_max_nr()['db_nr__max']
        if q:
            return q + 1
        else:
            return 0

    def db_free_nr(self):
        from itertools import chain
        min_max = set(range(0,self.new_db_nr()))
        return sorted(min_max.difference(set(chain.from_iterable(self.values_list('db_nr')))))


class Partnumber(TimeStampedModel):
    PCS = 'pcs'
    G = 'gr'
    M = 'mt'
    MM = 'mm'
    L = 'lt'
    UNIT = [
        (PCS, 'pezzi'),
        (G, 'grammi'),
        (M, 'metri'),
        (MM, 'millimetri'),
        (L, 'litri'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=60, unique=True, db_index=True)
    unit = models.CharField(choices=UNIT, default=PCS, max_length=4)
    description = models.TextField(blank=True)
    pmu = models.FloatField(null=True, blank=True)
    db_nr = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)

    objects = models.Manager()
    db = DbManager()
    
    def picking_area(self):
        return [
            iconcat([str(s) for s in i.storage.get_ancestors()], [str(i.storage)]) for i in self.item_set.filter(area='pg')
        ]

    def storage_area(self):
        return [
            iconcat([str(s) for s in i.storage.get_ancestors()], [str(i.storage)]) for i in self.item_set.filter(area='se')
        ]

    def __str__(self):
        return "{self.sku} | {self.category}".format(self=self)

    def related_label(self):
        return "%s" % self.sku

    def natural_key(self):
        return (self.sku,)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('partnumber_update', args=((self.id,)))

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "sku__icontains",)

    class Meta:
        ordering = ('sku',)
