from django.forms import Select, TextInput, CheckboxSelectMultiple

import django_filters

from partnumbers.models import Partnumber, Category


class PartnumberFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter(
        lookup_expr="contains",
        widget=TextInput(attrs={"class": "form-control"}),
        label="Codice",
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Filtra per categoria",
        label_suffix=":",
    )

    class Meta:
        model = Partnumber
        fields = ["sku", "category"]
