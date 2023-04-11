from django.urls import path

from . import views

urlpatterns = [
    path("inspection", views.LotCreateAPIView.as_view(), name="api-lot-create"),
]
