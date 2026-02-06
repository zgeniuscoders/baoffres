from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.viewsets import CategoryViewSet, LocationViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
