from rest_framework import serializers

from api.models import Category, Location


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
