from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'comptes', views.CompteViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'epargnes', views.EpargneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]