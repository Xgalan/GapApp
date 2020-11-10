import uuid

from django.db import models

from django_extensions.db.models import TimeStampedModel



class Category(TimeStampedModel):
    category_name = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return "%s" % self.category_name

    def __str__(self):
        return "%s" % self.category_name


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

    def __unicode__(self):
        return "%s" % self.sku

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
