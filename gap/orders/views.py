from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from core.views import StandardResultsSetPagination
from orders.models import Order, Orderitem
from orders.serializers import OrderSerializer, ItemSerializer



class OrderViewSet(ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.select_related('customer').all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'orders/api_list.html'
    filter_backends = [SearchFilter]
    search_fields  = ['coc']

    @action(
        detail=False,
        methods=['get']
    )
    def requested(self, request):
        q = Orderitem.groupby.isoweek_open()
        if request.accepted_renderer.format == 'html':
            return Response({'results': q}, template_name='orders/orderitem_list.html')
        return Response(q)


class OrderitemByPartnumber(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ItemSerializer

    def get_queryset(self):
        id_ = self.kwargs.get("pk")
        return Orderitem.objects.select_related(
                'coc', 'partnumber'
            ).filter(
                Q(status='planned') | Q(status='released'),
                partnumber=id_
            )


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, id=id_)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['items'] = Orderitem.objects.filter(coc=self.object.id).select_related('partnumber').all()
        return context