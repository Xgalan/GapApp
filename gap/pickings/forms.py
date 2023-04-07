from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from pickings.models import Picking


class PickingForm(forms.ModelForm):
    year = forms.IntegerField(
        required=False, label="Anno di ricerca", initial=datetime.now().year
    )

    class Meta:
        model = Picking
        fields = (
            "partnumber",
            "lot",
            "year",
            "picking_date",
            "picking_operator",
        )
        localized_fields = ("picking_date",)
        labels = {
            "partnumber": _("Codice"),
            "lot": _("Nr. Lotto"),
            "picking_date": _("Data immissione in area prelievo"),
            "picking_operator": _("Operatore"),
        }
        widgets = {
            "partnumber": forms.Select(attrs={"class": "form-control"}),
            "lot": forms.Select(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "picking_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
            ),
            "picking_operator": forms.Select(attrs={"class": "form-control-plaintext"}),
        }
