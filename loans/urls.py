from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'prets', views.PretViewSet)
router.register(r'remboursements', views.RemboursementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
