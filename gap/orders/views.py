from django.db.models import Q

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.accepted_renderer.format == 'html':
            items = Orderitem.objects.filter(
                coc=instance.id).select_related('partnumber').all()
            return Response({'object': instance, 'items': items}, template_name='orders/order_detail.html')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get']
    )
    def requested(self, request):
        q = Orderitem.groupby.isoweek_open()
        if request.accepted_renderer.format == 'html':
            return Response({'results': q}, template_name='orders/orderitem_list.html')
        return Response(q)

    @action(
        detail=True,
        methods=['get']
    )
    def bypartnumber(self, request, pk=None):
        id_ = pk
        q = Orderitem.objects.select_related(
                'coc', 'partnumber'
            ).filter(
                Q(status='planned') | Q(status='released'),
                partnumber=id_
            )
        if q is not None:
            serializer = ItemSerializer(q, many=True)
            if request.accepted_renderer.format == 'html':
                return Response({'results': q}, template_name='orders/order_by_partnumber.html')
            return Response(serializer.data)
