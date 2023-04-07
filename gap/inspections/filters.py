from django.forms import Select, NumberInput

import django_filters

from inspections.models import Lot
from core.mixins import SourceType


class LotFilter(django_filters.FilterSet):
    lot_number = django_filters.NumberFilter(
        lookup_expr="contains", widget=NumberInput(attrs={"class": "form-control"})
    )
    lot_date = django_filters.DateFromToRangeFilter()
    supplier_type = django_filters.ChoiceFilter(
        choices=SourceType.choices, widget=Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Lot
        fields = ["lot_number", "lot_date", "supplier_type"]
