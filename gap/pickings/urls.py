from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='picking_recents'),
    path('new/', views.CreateView.as_view(), name='picking_create'),
    path('new/<uuid:pk>/', views.CreateView.as_view(), name='picking_create_pn'),
    path('<int:pk>/', views.UpdateView.as_view(), name='picking_update'),
    path('partnumber/<uuid:pk>/', views.PickingListView.as_view(), name='picking_filter_pn'),
]