from django.urls import path

from . import views


urlpatterns = [
    path('<uuid:pk>/', views.UpdateView.as_view(), name='partnumber_update'),
    path('new/', views.CreateView.as_view(), name='partnumber_create'),
]