from django.urls import path

from . import views


urlpatterns = [
    path("", views.LotFilterView.as_view(), name="lot_list"),
    path(
        "detail/<int:pk>/", views.LotReadUpdateView.as_view(), name="lot_retrieveupdate"
    ),
    path("add/", views.CreateView.as_view(), name="lot_create"),
    path("add/<uuid:pn_id>/", views.CreateView.as_view(), name="lot_create_pn"),
]
