"""gap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework import routers
from rest_framework.schemas import get_schema_view

from partnumbers.views import PartnumberViewSet
from pickings.views import PickingViewSet
from orders.views import OrderViewSet



router = routers.DefaultRouter()
router.register(r'partnumbers', PartnumberViewSet, basename='partnumber')
router.register(r'pickings', PickingViewSet, basename='picking')
router.register(r'orders', OrderViewSet, basename='order')

schema_url_patterns = [
    path('api/', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('pickings/', include('pickings.urls')),
    path('partnumbers/', include('partnumbers.urls')),
    path('inspections/', include('inspections.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('openapi', get_schema_view(
        title="GappApp",
        description="OpenAPI schema for GapApp",
        version="0.1.0",
        patterns=schema_url_patterns
    ), name='openapi-schema'),
    path('', include('core.urls')),
] + schema_url_patterns


admin.site.site_header = "GAP - Gestione passaggio sottoassiemi e componenti in area prelievo"
admin.site.index_title = "Pannello di controllo"