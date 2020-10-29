from django.forms import ModelForm, Select, Textarea, NumberInput, TextInput
from django.utils.translation import gettext_lazy as _

from partnumbers.models import Partnumber



class PartnumberForm(ModelForm):
    class Meta:
        model = Partnumber
        fields = ('sku', 'description', 'unit', 'pmu', 'db_nr', 'category',)
        #localized_fields = ('pmu',)
        labels = {
            'sku': _('Codice'),
            'description': _('Descrizione'),
            'unit': _('Unità stock'),
            'pmu': _('P.M.U. (g)'),
            'db_nr': _('Nr. DB contapezzi'),
            'category': _('Categoria'),
        }
        widgets = {
            'sku': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'unit': Select(attrs={'class': 'form-control'}),
            'pmu': NumberInput(attrs={'class': 'form-control'}),
            'db_nr': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }
