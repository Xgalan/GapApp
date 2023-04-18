from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from django_filters.views import FilterView
from django_htmx.http import trigger_client_event

from partnumbers.models import Partnumber, Category
from partnumbers.forms import PartnumberForm
from partnumbers.filters import PartnumberFilter


class PartnumberPrintList(LoginRequiredMixin, FilterView):
    filterset_class = PartnumberFilter
    ordering = "sku"
    queryset = Partnumber.objects.select_related("category")

    def get_template_names(self):
        if self.request.htmx:
            if "Template" in self.request.headers:
                if self.request.headers["Template"] == "call_storage":
                    template_name = "print_storage.html"
        else:
            template_name = "print_list.html"

        return template_name


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
