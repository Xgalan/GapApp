from django.forms import ModelForm, Select, DateInput, NumberInput
from django.utils.translation import gettext_lazy as _

from inspections.models import Lot



class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = ('lot_number', 'lot_date', 'supplier_type',)
        localized_fields = ('lot_date',)
        labels = {
            'lot_number': _('Nr. Lotto'),
            'lot_date': _('Data consegna'),
            'supplier_type': _('Tipo fornitore'),
        }
        widgets = {
            'lot_number': NumberInput(attrs={'class': 'form-control'}),
            'lot_date': DateInput(attrs={'class': 'form-control'}),
            'supplier_type': Select(attrs={'class': 'form-control'}),
        }
