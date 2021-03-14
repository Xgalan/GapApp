from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>/', views.UpdateView.as_view(), name='picking_update'),
    path('add/', views.CreateView.as_view(), name='picking_create'),
    path('add/<uuid:pn_id>/', views.CreateView.as_view(), name='picking_create_pn'),
    path('add/<int:lot_id>/', views.CreateView.as_view(), name='picking_create_lot'),
    path('add/<uuid:pn_id>/<int:lot_id>/', views.CreateView.as_view(), name='picking_create_pn_lot'),
    path('partnumber/<uuid:pk>/', views.PickingListView.as_view(), name='picking_filter_pn'),
]