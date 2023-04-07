from django.views.generic import TemplateView

from rest_framework.pagination import PageNumberPagination


class HomeView(TemplateView):
    template_name = "home.html"


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100
