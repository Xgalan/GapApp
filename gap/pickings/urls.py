from django.urls import path

from . import views


urlpatterns = [
    path("", views.PickingFilterView.as_view(), name="picking_list"),
    path("add/", views.CreateView.as_view(), name="picking_create"),
    path("add/<uuid:pn_id>/", views.CreateView.as_view(), name="picking_create_pn"),
    path("add/<int:lot_id>/", views.CreateView.as_view(), name="picking_create_lot"),
    path(
        "add/<uuid:pn_id>/<int:lot_id>/",
        views.CreateView.as_view(),
        name="picking_create_pn_lot",
    ),
]
