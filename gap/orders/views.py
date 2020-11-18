from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from orders.models import Order, Orderitem



class OrderIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/orderitem_list.html'


class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        dates = Orderitem.objects.select_related('coc').filter(
            Q(status='planned') | Q(status='released')
        ).dates(
            'coc__shipdate', 'week', order='DESC'
        )
        weeks = [d.isocalendar()[1] for d in dates]
        objects = [{w: Orderitem.filterby.shipdate_in_isoweek_open(w).values(
            'id', 
            'partnumber', 
            'partnumber__sku', 
            'coc', 
            'coc__coc', 
            'coc__shipdate',
            'coc__customer',
            'quantity',
            'status',
            'status_changed'
        )} for w in weeks]
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