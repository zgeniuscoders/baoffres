from django.template.context_processors import request
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Category, Location, Job
from api.serializers import CategorySerializer, AddCategorySerializer, LocationSerializer, JobSerializer, \
    AddJobSerializer, JobListSerializer


@extend_schema_view(
    list=extend_schema(
        responses={200: CategorySerializer}
    ),
    retrieve=extend_schema(
        responses={200: CategorySerializer}
    ),
    create=extend_schema(
        responses={201: CategorySerializer},
        request=AddCategorySerializer,
    )
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("created_at", "updated_at", "name")
    ordering_fields = ("id", "created_at", "updated_at", "name")

    def get_serializer_class(self):
        if self.action == 'create':
            return AddCategorySerializer
        else:
            return CategorySerializer

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='categories'))
    def list(self, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='category'))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(self, *args, **kwargs)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("name",)
    ordering_fields = ("id", "created_at", "updated_at", "name")

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='location_list'))
    def list(self, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='location_detail'))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(self, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(
        request=AddJobSerializer,
        responses={201: JobSerializer},
    ),
    list=extend_schema(
        responses={200: JobListSerializer},
    ),
    retrieve=extend_schema(
        responses={200: JobSerializer},
    )
)
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("title", "category", "owner")
    ordering_fields = ("id", "created_at", "updated_at", "title")

    def get_serializer_class(self):
        if self.action == 'create':
            return AddJobSerializer
        elif self.action == 'retrieve':
            return JobSerializer
        else:
            return JobListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='jobs_list'))
    def list(self, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 24, key_prefix='job_detail'))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(self, *args, **kwargs)
