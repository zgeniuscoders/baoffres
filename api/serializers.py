from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Category, Location, Tag, Job


class AddCategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'created_at', 'updated_at')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class AddJobSerializer(serializers.ModelSerializer):
    category_id = (
        serializers.PrimaryKeyRelatedField(
            write_only=True,
            source="category",
            queryset=Category.objects.all())
    )

    locations = serializers.ListField(
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(
            queryset=Location.objects.all(),
        )
    )

    tags = serializers.ListField(
        write_only=True,
        child=serializers.CharField()
    )

    class Meta:
        model = Job
        fields = ('locations', 'tags', 'title', 'url', 'image', 'category_id')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        locations = validated_data.pop('locations')

        job = Job.objects.create(**validated_data)

        job.locations.set(locations)

        tag_objs = []
        for tag in tags:
            find_tag, new_tag = Tag.objects.get_or_create(name=tag.strip().lower())
            tag_objs.append(find_tag)

        job.tags.set(tag_objs)
        return job


class JobListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'slug', 'description', 'image', 'category', 'owner', 'created_at', 'updated_at')


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    locations = LocationSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'slug', 'description', 'image', 'locations', 'category', 'owner', 'created_at',
                  'updated_at', 'tags')
