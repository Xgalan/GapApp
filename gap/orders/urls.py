from django.urls import path

from . import views



urlpatterns = [
    path('', views.OrderIndexView.as_view(), name='order_list'),
    path('api/', views.OrderListView.as_view(), name='api_order_list'),
    #path('<int:year>/', views.OrderIndexView.as_view(), name="order_year_filter"),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]