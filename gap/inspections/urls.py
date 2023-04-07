from django.urls import path

from . import views


urlpatterns = [
    path("", views.LotFilterView.as_view(), name="lot_list"),
    path("<int:pk>/", views.LotReadUpdateView.as_view(), name="lot_retrieveupdate"),
    path("filter/", views.FilteredListView.as_view(), name="lot_filtered"),
    path("filter/<uuid:pn_id>/", views.FilteredListView.as_view(), name="lot_filtered"),
    path("add/", views.CreateView.as_view(), name="lot_create"),
    path("add/<uuid:pn_id>/", views.CreateView.as_view(), name="lot_create_pn"),
]
