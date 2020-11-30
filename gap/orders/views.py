from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, Orderitem
from orders.serializers import ItemSerializer



class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    paginate_by = 16


class OrderitemByWeekView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/orderitem_list.html'


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


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        objects = Orderitem.groupby.isoweek_open()
        return Response(objects)


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, id=id_)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['items'] = Orderitem.objects.filter(coc=self.object.id).select_related('partnumber').all()
        return context