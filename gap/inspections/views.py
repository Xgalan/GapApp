from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django_filters import rest_framework as filters

from core.views import StandardResultsSetPagination
from inspections.models import Lot
from inspections.forms import LotForm
from inspections.serializers import LotSerializer


class LotFilter(filters.FilterSet):
    class Meta:
        model = Lot
        fields = {
            "lot_number": ["exact", "contains"],
            "lot_date": ["year__gt"],
            "supplier_type": ["exact"]
        }


class ListView(ListAPIView):
    """  
    API endpoint that allows to retrieve a list of lots 
    """
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'inspections/list.html'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LotFilter


class UpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    model = Lot
    form_class = LotForm
    template_name_suffix = '_update_form'
    success_message = "Lotto %(lot)s aggiornato"
    success_url = reverse_lazy('lot_list')

    def form_invalid(self, form):
        errors = form.errors.as_data()['__all__'][0]
        messages.error(self.request, errors, extra_tags='danger')
        return super().form_invalid(form)
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            lot=str(self.object),
        )


class CreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = Lot
    form_class = LotForm
    template_name_suffix = '_create_form'
    success_message = "Lotto %(lot)s creato correttamente"

    def form_invalid(self, form):
        errors = form.errors.as_data()['__all__'][0]
        messages.error(self.request, errors, extra_tags='danger')
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            lot=str(self.object),
        )

    def get_success_url(self):
        pn_id = self.kwargs.get('pn_id')
        if pn_id:
            url_kwargs = {'pn_id': pn_id, 'lot_id': self.object.id}
            return reverse_lazy('picking_create_pn_lot', kwargs=url_kwargs)
        else:
            return reverse_lazy('lot_list')


class DetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Lot.objects.prefetch_related('partnumbers').all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(self.queryset, id=id_)
