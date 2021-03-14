from django.urls import path

from . import views



urlpatterns = [
    path('', views.ListView.as_view(), name='lot_list'),
    path('<int:pk>/', views.DetailView.as_view(), name='lot_detail'),
    path('add/', views.CreateView.as_view(), name='lot_create'),
    path('add/<uuid:pn_id>/', views.CreateView.as_view(), name='lot_create_pn'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='lot_update'),
]