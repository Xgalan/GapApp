from django.forms import ModelForm, Select, DateInput, NumberInput
from django.utils.translation import gettext_lazy as _

from inspections.models import Lot


class LotForm(ModelForm):
    error_css_class = "danger"

    class Meta:
        model = Lot
        fields = (
            "lot_number",
            "lot_date",
            "supplier_type",
        )
        localized_fields = ("lot_date",)
        labels = {
            "lot_number": _("Nr. Lotto"),
            "lot_date": _("Data consegna"),
            "supplier_type": _("Tipo fornitore"),
        }
        widgets = {
            "lot_number": NumberInput(
                attrs={"class": "form-control", "placeholder": "Nr. Lotto"}
            ),
            "lot_date": DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "pattern": "\d{4}-\d{2}-\d{2}",
                }
            ),
            "supplier_type": Select(attrs={"class": "form-control"}),
        }
