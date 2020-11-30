from django.urls import path

from . import views



urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('api/', views.OrderListAPIView.as_view(), name='api_order_list'),
    path('requested/', views.OrderitemByWeekView.as_view(), name='orderitem_by_week'),
    path('requested/<uuid:pk>/', views.OrderitemByPartnumber.as_view(), name='orderitem_by_pn'),
    #path('<int:year>/', views.OrderIndexView.as_view(), name="order_year_filter"),
]