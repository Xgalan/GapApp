import django_filters

from pickings.models import Picking


class PickingFilter(django_filters.FilterSet):
    picking_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Picking
        fields = {
            "partnumber__sku": ["icontains"],
            "partnumber__id": ["exact"],
        }

    @property
    def qs(self):
        parent = super().qs
        picking_operator = getattr(self.request, "user", None)
        if picking_operator.is_staff:
            return parent
        return parent.filter(picking_operator=picking_operator)
