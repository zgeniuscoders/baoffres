from rest_framework import serializers

from api.models import Category


class AddCategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'created_at', 'updated_at')
