from rest_framework import serializers

from api.serializers import CategoryGetSerializer
from shop.models import Product


class ProductGetSerializer(serializers.ModelSerializer):
    category = CategoryGetSerializer()

    class Meta:
        model = Product
        fields = ['id', 'product', 'price', 'description', 'category', 'balance']
        read_only = ['id']


class ProductPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'product', 'price', 'description', 'category', 'balance']
        read_only = ['id']
