from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from rest_framework.generics import ListAPIView
from rest_framework import permissions

from pickings.models import Picking
from pickings.serializers import PickingSerializer
from pickings.forms import PickingForm



class PickingListView(ListAPIView):
    """
    API endpoint that retrieves all the pickings with a specified partnumber.
    """
    serializer_class = PickingSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        """
        This view should return a list of all the pickings for
        the partnumber as determined by the uuid portion of the URL.
        """
        id_ = self.kwargs['pk']
        return Picking.objects.filter(partnumber__id=id_)


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'pickings/list.html'
    context_object_name = 'pickings_list'

    def get_queryset(self):
        """Return the last ten pickings."""
        if self.request.user.is_staff:
            return Picking.objects.order_by('-modified')[:20]
        else:
            return Picking.objects.filter(
                picking_operator=self.request.user).order_by('-modified')[:20]


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Picking
    form_class = PickingForm
    template_name_suffix = '_create_form'

    def form_invalid(self, form):
        errors = form.errors.as_data()['__all__'][0]
        messages.error(self.request, errors, extra_tags='danger')
        return super().form_invalid(form)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        pn_id = self.kwargs.get('pn_id')
        lot_id = self.kwargs.get('lot_id')
        kwargs['initial']['picking_operator'] = self.request.user
        if pn_id:
            kwargs['initial']['partnumber'] = pn_id
        if lot_id:
            kwargs['initial']['lot'] = lot_id
        return kwargs


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Picking
    form_class = PickingForm
    template_name_suffix = '_update_form'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Picking, id=id_)
