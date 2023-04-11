from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django_filters.views import FilterView

from pickings.models import Picking
from pickings.forms import PickingForm
from pickings.filters import PickingFilter


class PickingFilterView(LoginRequiredMixin, FilterView):
    filterset_class = PickingFilter
    ordering = "-picking_date"
    queryset = Picking.objects.select_related("partnumber", "lot", "picking_operator")
    paginate_by = 25

    def get_template_names(self):
        if self.request.htmx:
            template_name = "picking_filter_partial.html"
        else:
            template_name = "picking_filter.html"

        return template_name


class CreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = Picking
    form_class = PickingForm
    template_name_suffix = "_create_form"
    success_message = "Movimento %(picking)s creato correttamente"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            picking=str(self.object),
        )

    def form_invalid(self, form):
        errors = form.errors
        if "__all__" in errors:
            errors = form.non_field_errors()
        messages.error(self.request, errors, extra_tags="danger")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "picking_list",
        )

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        pn_id = self.kwargs.get("pn_id")
        lot_id = self.kwargs.get("lot_id")
        kwargs["initial"]["picking_operator"] = self.request.user
        if pn_id:
            kwargs["initial"]["partnumber"] = pn_id
        if lot_id:
            kwargs["initial"]["lot"] = lot_id
        return kwargs
