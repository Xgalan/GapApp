from django.urls import path

from . import views



urlpatterns = [
    path('', views.ListView.as_view(), name='lot_list'),
    path('add/', views.CreateView.as_view(), name='lot_create'),
    path('add/<uuid:pn_id>/', views.CreateView.as_view(), name='lot_create_pn'),
    path('<int:pk>/', views.DetailView.as_view(), name='lot_detail'),
    path('api/', views.ListAPIView.as_view(), name='api_lot_list'),
]