from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from partnumbers.models import Partnumber, Category
from partnumbers.forms import PartnumberForm
from partnumbers.serializers import PartnumberSerializer



class PartnumberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """
    queryset = Partnumber.objects.all()
    serializer_class = PartnumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku']


class IndexView(LoginRequiredMixin, generic.ListView):
    paginate_by = 16
    template_name = 'partnumbers/list.html'
    context_object_name = 'partnumbers_list'

    def get_queryset(self):
        return Partnumber.objects.select_related('category').order_by('sku')


class PrintListView(LoginRequiredMixin, generic.ListView):
    template_name = 'partnumbers/print_list.html'
    context_object_name = 'partnumbers_list'

    def get_queryset(self):
        return Partnumber.objects.order_by('sku')


class PrintDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'partnumbers/print_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Partnumber, id=id_)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['pickings'] = self.object.picking_set.order_by('-picking_date')
        return context


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Partnumber
    form_class = PartnumberForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Find the MAX db_nr
        q = Partnumber.objects.all().aggregate(Max('db_nr'))['db_nr__max']
        if q:
            context['new_db_nr'] = q + 1
        else:
            context['new_db_nr'] = 0
        return context


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Partnumber
    form_class = PartnumberForm
    template_name_suffix = '_update_form'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Partnumber, id=id_)
