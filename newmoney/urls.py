from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="NewMoney API",
        default_version='v1',
        description="API de gestion financière NewMoney - Système de microfinance",
        contact=openapi.Contact(email="contact@newmoney.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # Documentation API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints - TOUTES LES ROUTES DES APPLICATIONS
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/agents/', include('agents.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/loans/', include('loans.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    
    # DRF browsable API
    path('api-auth/', include('rest_framework.urls')),
]