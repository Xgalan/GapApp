from datetime import datetime

from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_htmx.http import trigger_client_event

from core.views import StandardResultsSetPagination
from partnumbers.models import Partnumber, Category
from partnumbers.forms import PartnumberForm
from partnumbers.serializers import PartnumberSerializer


class PartnumberViewSet(ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """

    queryset = Partnumber.objects.select_related("category")
    serializer_class = PartnumberSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["sku"]

    @action(detail=False, methods=["post"], renderer_classes=[TemplateHTMLRenderer])
    def search_by_sku(self, request):
        if request.htmx:
            results = Partnumber.objects.filter(
                sku__icontains=request.POST.get("search-by-sku")
            )
            serializer = self.get_serializer(results, many=True)
            return trigger_client_event(
                Response(
                    {"partnumbers": serializer.data},
                    template_name="partnumbers_options.html",
                ),
                "searchSkuCompleted",
                None,
                after="swap",
            )
        return Response(
            {"warning": "only HTMX requests are permitted on this endpoint"}
        )

    @action(detail=False, methods=["get"], renderer_classes=[TemplateHTMLRenderer])
    def print_storage(self, request):
        q = Partnumber.objects.select_related("category").exclude(
            category__category_name="Prodotto Finito"
        )
        results = [
            {
                "pk": p.id,
                "sku": p.sku,
                "category": p.category,
                "picking_area": p.picking_area(),
                "storage_area": p.storage_area(),
            }
            for p in q
        ]
        return Response(
            {"partnumbers_list": results}, template_name="print_storage.html"
        )

    @action(detail=False, methods=["get"], renderer_classes=[TemplateHTMLRenderer])
    def print_list(self, request):
        q = (
            Partnumber.objects.select_related("category")
            .exclude(
                Q(category__category_name="Prodotto Finito")
                | Q(category__category_name="Materiale di consumo")
                | Q(category__category_name="Bimetallo in nastro")
            )
            .order_by("sku")
        )
        return Response({"partnumbers_list": q}, template_name="print_list.html")

    @action(detail=True, methods=["get"], renderer_classes=[TemplateHTMLRenderer])
    def print_detail(self, request, pk=None):
        instance = self.get_object()
        year = self.request.query_params.get("year")
        if year:
            current_year = int(year)
        else:
            current_year = datetime.now().year
        past_year = current_year - 1
        past_year_picking = list(
            instance.picking_set.filter(picking_date__year=past_year).order_by(
                "-picking_date"
            )[:1]
        )
        current_year_pickings = list(
            instance.picking_set.filter(picking_date__year=current_year).order_by(
                "picking_date"
            )
        )
        pickings = past_year_picking + current_year_pickings
        if request.accepted_renderer.format == "html":
            # load other context data
            return Response(
                {
                    "object": instance,
                    "pickings": pickings,
                    "dates": [
                        d.year
                        for d in instance.picking_set.dates("picking_date", "year")
                    ],
                    "storages": {
                        "pg": instance.picking_area(),
                        "se": instance.storage_area(),
                    },
                },
                template_name="print_detail.html",
            )
        return Response({"warning": "only HTML response permitted on this endpoint"})


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Partnumber
    form_class = PartnumberForm
    template_name_suffix = "_create_form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_db_nr"] = Partnumber.db.new_db_nr()
        context["db_free_nr"] = Partnumber.db.db_free_nr()
        return context


class PartnumberDetailView(LoginRequiredMixin, generic.DetailView):
    model = Partnumber
    queryset = Partnumber.objects.select_related("category")

    def get_template_names(self):
        if self.request.htmx:
            template_name = "partnumber_detail_partial.html"
        else:
            template_name = "partnumbers/partnumber_detail.html"
        return template_name


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Partnumber
    form_class = PartnumberForm

    def get_template_names(self):
        if self.request.htmx:
            template_name = "partnumber_form_partial.html"
        else:
            from django.core.exceptions import BadRequest
            raise BadRequest
        return template_name

    def get_success_url(self):
        return reverse("partnumber_detail", kwargs={"pk": self.kwargs.get("pk")})

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Partnumber, id=id_)
