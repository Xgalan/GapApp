from datetime import date, datetime
from calendar import monthrange
from operator import ge

from django.db import models
from django.db.models import Q, Sum, F, Prefetch
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from core.mixins import ValuesMixin
from partnumbers.models import Partnumber



class RequestedManager(models.Manager):
    def this_year(self):
        current_year = date.today().year
        return self.filter(orderdate__year=current_year)

    def shipdate_in_range(self, start_date, end_date):
        format = "%Y-%m-%d"
        if type(start_date) is not datetime:
            start = datetime.strptime(start_date, format)
        else:
            start = start_date
        if type(end_date) is not datetime:
            end = datetime.strptime(end_date, format)
        else:
            end = end_date
        return self.filter(shipdate__range=(start, end))

    def shipdate_in_isoweek(self, isoweek):
        """
        Return an Order Queryset for the given iso week number.

        * isoweek must be an integer from 1 to 52.
        """
        if (isoweek > 52) or (isoweek < 1):
            raise ValueError('isoweek could not be greater than 52 or less than 1.')
        dates_query = self.dates('shipdate', 'day')
        dates = [x for x in dates_query if x.isocalendar()[1] == isoweek]
        return self.filter(shipdate__in=dates)

    def shipdate_in_month_range(self, start_month, end_month):
        """
        Return an Order Queryset from the first month requested to the last
        month requested.

        * start_month, end_month must be integers from 1 to 12.
        """

        if start_month >= end_month:
            raise ValueError('start_month could not be greater or equal to end_month')
        elif (start_month < 1 or end_month < 1) or (start_month > 12 or end_month > 12):
            raise ValueError('start_month and end_month must be from 1 to 12')

        start_date = date(date.today().year, start_month, 1)
        end_date = date(date.today().year, end_month, monthrange(date.today().year, end_month)[1])
        return self.shipdate_in_range(start_date, end_date)


class Company(ValuesMixin, TimeStampedModel):
    name = models.CharField(
        max_length=120,
        unique=True
    )

    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])

    class Meta:
        ordering = ('name',)
        verbose_name = 'company'
        verbose_name_plural = 'companies'


class Order(ValuesMixin, TimeStampedModel):
    """ 
    This model represent an order from a customer. 
    """
    coc = models.CharField(
        "nr COC", max_length=60,
        db_index=True
    )
    orderdate = models.DateField(
        "order date",
        db_index=True
    )
    shipdate = models.DateField(
        "shipment date",
        db_index=True
    )
    customer = models.ForeignKey(
        Company,
        on_delete=models.RESTRICT
    )
    items = models.ManyToManyField(
        Partnumber,
        through='Orderitem'
    )

    def __str__(self):
        return "COC: {self.coc} | {self.orderdate}".format(self=self)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    objects = models.Manager()
    requested = RequestedManager()

    class Meta:
        ordering = ('orderdate',)
        get_latest_by = 'orderdate'


class OrderitemsFilter(models.Manager):
    """ Filter by specific arguments. """

    def status_changed_in_range(self, start_date, end_date, status):
        format = "%Y-%m-%d"
        if type(start_date) is not datetime:
            start = datetime.strptime(start_date, format)
        else:
            start = start_date
        if type(end_date) is not datetime:
            end = datetime.strptime(end_date, format)
        else:
            end = end_date
        return self.filter(status_changed__range=(start, end), status=status)

    def shipdate_in_range(self, start_date, end_date):
        return self.filter(
            Q(status='planned') | Q(status='released'),
            coc__in=Order.requested.shipdate_in_range(start_date, end_date).values('id'))

    def shipdate_in_isoweek(self, isoweek):
        return self.filter(coc__in=Order.requested.shipdate_in_isoweek(isoweek).values('id'))
    
    def shipdate_in_isoweek_open(self, isoweek):
        return self.select_related('coc').filter(
            Q(status='planned') | Q(status='released'),
            coc__in=Order.requested.shipdate_in_isoweek(isoweek).values('id')
        )

    def shipdate_in_month_range(self, start_month, end_month):
        return self.filter(coc__in=Order.requested.shipdate_in_month_range(
            start_month, end_month).values('id'))


class OrderitemsGroupBy(models.Manager):
    """ Various aggregates """

    def total_status_open(self):
        total = Sum('quantity', filter=Q(status='planned') | Q(status='released'))
        return self.select_related(
            'partnumber'
        ).values(
            'partnumber__sku'
        ).order_by(
            'partnumber'
        ).annotate(
            total=total
        )

    def isoweek_open(self):
        """ Group items in order by isoweek """

        dates = self.select_related('coc').filter(
            Q(status='planned') | Q(status='released')
        ).dates('coc__shipdate', 'week', order='DESC')
        weeks = [d.isocalendar()[:2] for d in dates]
        return [
            {
                "{w[1]} - {w[0]}".format(w=w): Orderitem.filterby.shipdate_in_isoweek_open(
                    w[1] # ISO week
                ).values(
                    'partnumber',
                    'partnumber__sku',
                ).order_by(
                    'partnumber__sku'
                ).annotate(
                    total=Sum('quantity')
                )
            } for w in weeks
        ]


class Orderitem(TimeStampedModel):
    """
    This model represent the product requested by the customer in a related order.
    """
    class OrderitemStatus(models.TextChoices):
        PLANNED = 'planned', _('In programma')
        RELEASED = 'released', _('In produzione')
        CLOSED = 'closed', _('Evaso')
        DELETED = 'deleted', _('Annullato')

    partnumber = models.ForeignKey(
        Partnumber,
        verbose_name="Finished Good",
        on_delete=models.RESTRICT
    )
    coc = models.ForeignKey(
        Order,
        verbose_name="COC",
        on_delete=models.RESTRICT
    )
    status = models.CharField(
        choices=OrderitemStatus.choices,
        default=OrderitemStatus.PLANNED,
        max_length=12
    )
    status_changed = models.DateTimeField(
        editable=False,
        default=timezone.now
    )
    quantity = models.IntegerField("pcs ordered")

    def save(self, *args, **kwargs):
        """
        update the date when the order status of the item changes.
        """
        try:
            old_object = Orderitem.objects.get(id=self.id)
            if old_object.status != self.status:
                self.status_changed = timezone.now()
        except Orderitem.DoesNotExist:
            pass
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return "{self.partnumber} | {self.coc} | Q.ty: {self.quantity} | {self.status}".format(self=self)

    def get_absolute_url(self):
        return reverse('orderitem-detail', args=[str(self.coc.id)])

    objects = models.Manager()
    filterby = OrderitemsFilter()
    groupby = OrderitemsGroupBy()

    class Meta:
        verbose_name = "finished good"
        verbose_name_plural = "finished goods ordered"