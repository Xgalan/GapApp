from django.urls import path

from . import views



urlpatterns = [
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('requested/<uuid:pk>/', views.OrderitemByPartnumber.as_view(), name='orderitem_by_pn'),
    #path('<int:year>/', views.OrderIndexView.as_view(), name="order_year_filter"),
]