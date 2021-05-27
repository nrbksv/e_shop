from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import ProductGetSerializer, OrderGetSerializer, OrderPostSerializer, OrderGetProductSerializer, \
    OrderPostProductSerializer, ProductPostSerializer
from shop.models import Product, Order


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductGetSerializer

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            self.serializer_class = ProductPostSerializer
        return super().dispatch(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer

    def create(self, request, *args, **kwargs):
        products = request.data.get('products')
        prod_list = [i.get('products') for i in products]
        order_dict = {
            'user_name': request.data.get('user_name'),
            'user_phone': request.data.get('user_phone'),
            'user_address': request.data.get('user_address'),
            'products': prod_list
        }
        order = OrderPostSerializer(data=order_dict)
        if order.is_valid():
            order_1 = order.save()
        else:
            return Response(order.errors, status=400)

        for i in products:
            data_dict = {
                'order': order_1.id,
                'products': i.get('products'),
                'quantity': i.get('quantity')
            }
            order_prods = OrderPostProductSerializer(data=data_dict)
            if order_prods.is_valid():
                order_prods.save()
            else:
                return Response(order_prods.errors, status=400)
        return Response(order.data)
