from datetime import datetime

from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from core.views import StandardResultsSetPagination
from partnumbers.models import Partnumber, Category
from partnumbers.forms import PartnumberForm
from partnumbers.serializers import PartnumberSerializer



class PartnumberViewSet(ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """
    queryset = Partnumber.objects.select_related('category').all()
    serializer_class = PartnumberSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'partnumbers/api_list.html'
    filter_backends = [SearchFilter]
    search_fields = ['sku']

    @action(
        detail=False,
        methods=['get'],
        renderer_classes=[TemplateHTMLRenderer]
    )
    def print_list(self, request):
        q = Partnumber.objects.select_related('category').exclude(
            Q(category__category_name='Prodotto Finito') | 
            Q(category__category_name='Materiale di consumo')
            ).order_by('sku')
        return Response({'partnumbers_list': q}, template_name='partnumbers/print_list.html')
    
    @action(
        detail=False,
        methods=['get']
    )
    def category_filter(self, request):
        #TODO: add option for filtering objects based on category
        pass


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Partnumber
    form_class = PartnumberForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Find the MAX db_nr
        q = Partnumber.objects.all().aggregate(Max('db_nr'))['db_nr__max']
        if q:
            context['new_db_nr'] = q + 1
        else:
            context['new_db_nr'] = 0
        return context


class PrintDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'partnumbers/print_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Partnumber, id=id_)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get("year")
        if year:
            current_year = year
        else:
            current_year = datetime.now().year
        past_year = current_year - 1
        past_year_picking = list(self.object.picking_set.filter(
            picking_date__year=past_year).order_by('-picking_date')[:1])
        current_year_pickings = list(self.object.picking_set.filter(
            picking_date__year=current_year).order_by('picking_date'))
        context['pickings'] = past_year_picking + current_year_pickings
        context['dates'] = [d.year for d in self.object.picking_set.dates('picking_date', 'year')]

        from operator import iconcat
        pg = [iconcat([str(s) for s in i.storage.get_ancestors()], [str(i.storage)]) for i in self.object.item_set.filter(area='pg')]
        se = [iconcat([str(s) for s in i.storage.get_ancestors()], [str(i.storage)]) for i in self.object.item_set.filter(area='se')]
        context['storages'] = {
            "pg": pg,
            "se": se
        }
        return context


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Partnumber
    form_class = PartnumberForm
    template_name_suffix = '_update_form'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Partnumber, id=id_)
