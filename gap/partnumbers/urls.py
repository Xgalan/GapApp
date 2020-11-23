from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='partnumber_list'),
    path('<uuid:pk>/', views.UpdateView.as_view(), name='partnumber_update'),
    path('new/', views.CreateView.as_view(), name='partnumber_create'),
    path('print/', views.PrintListView.as_view(), name='partnumber_print'),
    path('print/<uuid:pk>/', views.PrintDetailView.as_view(), name='partnumber_detail'),
    path('print/<uuid:pk>/<int:year>/', views.PrintDetailView.as_view(), name='partnumber_detail_year'),
]