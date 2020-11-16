from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from inspections.models import Lot
from inspections.forms import LotForm



class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Lot
    form_class = LotForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('picking_recents')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        return super().form_invalid(form)
