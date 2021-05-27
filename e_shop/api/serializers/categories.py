from rest_framework import serializers

from shop.models import Category


class CategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']

    def to_representation(self, instance):
        return instance.category


class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']
