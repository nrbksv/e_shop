from rest_framework import serializers

from api.serializers import UserSerializer, OrderGetProductSerializer, OrderPostProductSerializer
from shop.models import Order


class OrderGetSerializer(serializers.ModelSerializer):
    _user = UserSerializer()
    products = OrderGetProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'user_name', 'user_phone', 'user_address', '_user']


class OrderPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'product', 'user_name', 'user_phone', 'user_address', '_user']
