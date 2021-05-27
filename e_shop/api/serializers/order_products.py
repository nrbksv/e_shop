from rest_framework import serializers

from api.serializers import ProductGetSerializer
from shop.models import OrderProduct


class OrderGetProductSerializer(serializers.ModelSerializer):
    products = ProductGetSerializer()

    class Meta:
        model = OrderProduct
        fields = ['products', 'quantity']


class OrderPostProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['products', 'order', 'quantity']

