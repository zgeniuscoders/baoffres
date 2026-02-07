from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.viewsets import CategoryViewSet, LocationViewSet, JobViewSet, UserViewSet, RegisterUserView, KubernateViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('locations', LocationViewSet)
router.register('jobs', JobViewSet)
router.register('users', UserViewSet)
router.register(f'', KubernateViewSet, basename='kubernates')

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterUserView.as_view()),
]
