from django.forms import ModelForm, Select, DateInput
from django.utils.translation import gettext_lazy as _

from pickings.models import Picking



class PickingForm(ModelForm):
    class Meta:
        model = Picking
        fields = ('partnumber', 'lot', 'picking_date', 'picking_operator',)
        localized_fields = ('picking_date',)
        labels = {
            'partnumber': _('Codice'),
            'lot': _('Nr. Lotto'),
            'picking_date': _('Data immissione in area prelievo'),
            'picking_operator': _('Operatore')
        }
        widgets = {
            'partnumber': Select(attrs={'class': 'form-control'}),
            'lot': Select(attrs={'class': 'form-control'}),
            'picking_date': DateInput(attrs={'class': 'form-control'}),
            'picking_operator': Select(attrs={'class': 'form-control'}),
        }
