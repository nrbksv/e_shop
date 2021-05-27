import json

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ProductGetSerializer, OrderGetSerializer, OrderPostSerializer, \
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


class Cart(APIView):

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        if cart:
            json_cart = json.dumps(cart)
            return HttpResponse(json_cart)
        return JsonResponse({'error': 'cart is empty'}, status=400)

    def post(self, request, *args, **kwargs):
        if not request.session.get('cart'):
            request.session['cart'] = dict()
        cart = request.session.get('cart')
        if request.body:
            data = json.loads(request.body)
            product = get_object_or_404(Product, id=data['product'])
            if product.balance - data['quantity'] >= 0:
                if not cart.get(str(product.id)):
                    cart[str(data['product'])] = data['quantity']
                else:
                    cart[str(data['product'])] += data['quantity']
                request.session['cart'] = cart
                return JsonResponse(data)
            return JsonResponse({'error': f'Ordered: {data["quantity"]} In stock: {product.balance}'}, status=400)
        return JsonResponse({'error': 'no data'}, status=400)

    def delete(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        if request.body:
            data = json.loads(request.body)
            if cart:
                if cart.get(str(data['product'])):
                    balance = cart[str(data['product'])] - data['quantity']
                    if balance <= 0:
                        del cart[str(data['product'])]
                    cart[str(data['product'])] = balance
                    request.session['cart'] = cart
                    return JsonResponse({'response': 'ok'})
                return JsonResponse({'error': 'no such product'}, status=400)
        return JsonResponse({'error': 'no data'}, status=400)


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse({'aaa': 'asdasd'})
    return HttpResponseNotAllowed('Only GET request are allowed')






