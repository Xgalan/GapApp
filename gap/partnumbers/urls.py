from django.urls import path

from . import views


urlpatterns = [
    path("", views.PartnumberPrintList.as_view(), name="partnumber_print_list"),
    path("new/", views.CreateView.as_view(), name="partnumber_create"),
    path("<uuid:pk>/", views.PartnumberDetailView.as_view(), name="partnumber_detail"),
    path("update/<uuid:pk>/", views.UpdateView.as_view(), name="partnumber_update"),
]
