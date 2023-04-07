from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_htmx.http import trigger_client_event
from django_filters.views import FilterView

from core.views import StandardResultsSetPagination
from inspections.models import Lot
from inspections.forms import LotForm
from inspections.serializers import LotSerializer, SingleLotSerializer
from inspections.filters import LotFilter
from partnumbers.models import Partnumber


class LotFilterView(LoginRequiredMixin, FilterView):
    filterset_class = LotFilter
    ordering = "-lot_date"
    queryset = Lot.objects.prefetch_related("partnumbers")
    paginate_by = 25

    def get_template_names(self):
        if self.request.htmx:
            template_name = "lot_filter_partial.html"
        else:
            template_name = "lot_filter.html"

        return template_name


class LotFilterDRF(filters.FilterSet):
    lot_date_range = filters.DateFromToRangeFilter(field_name="lot_date")

    class Meta:
        model = Lot
        fields = {
            "lot_number": ["exact", "contains"],
            "lot_date": ["year__gte"],
            "supplier_type": ["exact"],
        }


class FilteredListView(ListCreateAPIView):
    """
    API endpoint that retrieves lots filtered by valid sources.
    """

    serializer_class = LotSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "inspections/list.html"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LotFilterDRF

    def get_queryset(self):
        if "pn_id" in self.kwargs:
            pk = self.kwargs.get("pn_id")
            p = Partnumber.objects.get(id=pk)
            sources = set([s.shortform for s in p.category.sources.all()])
            q = Lot.objects.filter(supplier_type__in=sources)
            return q
        else:
            return Lot.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.htmx:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(
                {"inspections": serializer.data},
                template_name="lot_search_results.html",
            )
            return trigger_client_event(
                response,
                "lotSearchCompleted",
                None,
                after="swap",
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LotReadUpdateView(RetrieveUpdateAPIView):
    """
    API endpoint that implements Read and Update as in CRUD acronym.
    """

    queryset = Lot.objects.prefetch_related("partnumbers").all()
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
