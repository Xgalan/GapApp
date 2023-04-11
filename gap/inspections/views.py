from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django_htmx.http import trigger_client_event
from django_filters.views import FilterView

from inspections.models import Lot
from inspections.forms import LotForm
from restapi.serializers import SingleLotSerializer
from inspections.filters import LotFilter


class LotFilterView(LoginRequiredMixin, FilterView):
    """Used for endpoint "inspections/", django url name="lot_list" """

    filterset_class = LotFilter
    ordering = "-lot_date"
    queryset = Lot.objects.prefetch_related("partnumbers")
    paginate_by = 25

    def get_template_names(self):
        if self.request.htmx:
            if "Template" in self.request.headers:
                if self.request.headers["Template"] == "lot_options":
                    template_name = "lot_options.html"
            else:
                template_name = "lot_filter_partial.html"
        else:
            template_name = "lot_filter.html"

        return template_name


class LotReadUpdateView(RetrieveUpdateAPIView):
    """
    API endpoint that implements Read and Update as in CRUD acronym.
    """

    queryset = Lot.objects.prefetch_related(
        "picking_set__partnumber", "picking_set__picking_operator"
    )
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = SingleLotSerializer

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        if request.accepted_renderer.format == "html":
            return Response(
                {"lot": serializer.data},
                template_name="inspections/lot_retrieveupdate.html",
            )
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if request.htmx:
            response = Response(
                {"lot": serializer.data},
                template_name="inspections/retrieveupdate_partial.html",
            )
            return trigger_client_event(
                response,
                "updatedLot",
                {"lot_display": serializer.data["lot_display"]},
                after="swap",
            )
        return Response(serializer.data)


class CreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    model = Lot
    form_class = LotForm
    template_name_suffix = "_create_form"
    success_message = "Lotto %(lot)s creato correttamente"

    def form_invalid(self, form):
        errors = form.errors
        if "__all__" in errors:
            errors = form.non_field_errors()
        messages.error(self.request, errors, extra_tags="danger")
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            lot=str(self.object),
        )

    def get_success_url(self):
        pn_id = self.kwargs.get("pn_id")
        if pn_id:
            url_kwargs = {"pn_id": pn_id, "lot_id": self.object.id}
            return reverse_lazy("picking_create_pn_lot", kwargs=url_kwargs)
        else:
            url_kwargs = {"pk": self.object.id}
            return reverse_lazy("lot_retrieveupdate", kwargs=url_kwargs)
