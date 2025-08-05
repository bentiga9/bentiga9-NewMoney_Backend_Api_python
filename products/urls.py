from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conditions', views.ConditionViewSet)
router.register(r'produits', views.ProduitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]