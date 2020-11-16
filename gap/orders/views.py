from django.views.generic.dates import ArchiveIndexView
from django.views.generic import DetailView, YearArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Order, Orderitem
from .serializers import OrderSerializer, ProductSerializer



class OrderIndexView(LoginRequiredMixin, ArchiveIndexView):
    model = Order
    date_field = 'orderdate'
    date_list_period = 'year'
    paginate_by = 12
    queryset = Order.objects.select_related('customer').all()
    context_object_name = 'orders'


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Order, id=id_)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['items'] = Orderitem.objects.filter(coc=self.object.id).select_related('partnumber').all()
        return context


class OrderYearView(LoginRequiredMixin, YearArchiveView):
    queryset = Order.objects.select_related('customer').all()
    date_field = 'orderdate'
    paginate_by = 12
    template_name = 'orders/order_archive.html'
    context_object_name = 'orders'
    make_object_list = True
    allow_future = True