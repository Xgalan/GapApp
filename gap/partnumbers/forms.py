from django import forms
from django.utils.translation import gettext_lazy as _

from partnumbers.models import Partnumber


class PartnumberForm(forms.ModelForm):
    class Meta:
        model = Partnumber
        fields = (
            "sku",
            "description",
            "unit",
            "pmu",
            "db_nr",
            "category",
        )
        # localized_fields = ('pmu',)
        labels = {
            "sku": _("Codice"),
            "description": _("Descrizione"),
            "unit": _("Unità stock"),
            "pmu": _("P.M.U. (g)"),
            "db_nr": _("Nr. DB contapezzi"),
            "category": _("Categoria"),
        }
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "pmu": forms.NumberInput(attrs={"class": "form-control"}),
            "db_nr": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
