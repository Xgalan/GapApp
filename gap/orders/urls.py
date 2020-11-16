from django.urls import path

from . import views



urlpatterns = [
    path('', views.OrderIndexView.as_view(), name='order_list'),
    path('<int:year>/', views.OrderYearView.as_view(), name="order_year_archive"),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]