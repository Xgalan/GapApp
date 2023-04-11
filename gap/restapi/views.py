from datetime import datetime

from django.db.models import Q

from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django_htmx.http import trigger_client_event

from restapi import serializers
from inspections.models import Lot
from partnumbers.models import Partnumber
from warehouse.models import Storage


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class LotCreateAPIView(CreateAPIView):
    """API endpoint for creating a new Lot."""

    serializer_class = serializers.LotSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lot.objects.prefetch_related("partnumbers")


class PartnumberViewSet(ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """

    queryset = Partnumber.objects.select_related("category")
    serializer_class = serializers.PartnumberSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["sku"]

    @action(detail=False, methods=["get"], renderer_classes=[TemplateHTMLRenderer])
    def valid_supplier(self, request):
        if request.htmx:
            pk = request.GET.get("partnumber-id")
            if pk:
                qs = (
                    Partnumber.objects.select_related("category")
                    .get(id=pk)
                    .category.sources.all()
                )
            valid_sources = qs or None
            return Response(
                {"sources": valid_sources},
                template_name="partnumbers/sources_options.html",
            )
        return Response(
            {"warning": "only HTMX requests are permitted on this endpoint"}
        )

    @action(detail=False, methods=["get"], renderer_classes=[TemplateHTMLRenderer])
    def select_options(self, request):
        if request.htmx:
            if request.GET.get("search-by-sku"):
                template_name = "partnumbers_options.html"
                search_term = request.GET.get("search-by-sku")
                event = "searchSkuCompleted"
            else:
                template_name = "partnumbers/partnumber_select_options.html"
                search_term = request.GET.get("sku-icontains")
                event = "searchSkuCompleted"
            results = Partnumber.objects.filter(sku__icontains=search_term)
            serializer = self.get_serializer(results, many=True)
            return trigger_client_event(
                Response(
                    {"partnumbers": serializer.data},
                    template_name=template_name,
                ),
                event,
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
            instance.picking_set.select_related("lot")
            .filter(picking_date__year=past_year)
            .order_by("-picking_date")[:1]
        )
        current_year_pickings = list(
            instance.picking_set.select_related("lot")
            .filter(picking_date__year=current_year)
            .order_by("picking_date")
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
                        for d in instance.picking_set.select_related("lot").dates(
                            "picking_date", "year"
                        )
                    ],
                    "storages": {
                        "pg": instance.picking_area(),
                        "se": instance.storage_area(),
                    },
                },
                template_name="print_detail.html",
            )
        return Response({"warning": "only HTML response permitted on this endpoint"})


class StorageViewSet(ModelViewSet):
    """
    API endpoint that allows partnumbers to be viewed or edited.
    """

    queryset = Storage.objects.prefetch_related("items").all()
    serializer_class = serializers.StorageSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [
        JSONRenderer,
    ]
