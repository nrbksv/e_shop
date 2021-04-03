from django.views.generic import CreateView,ListView
from django.shortcuts import redirect, render, reverse, get_object_or_404

from shop.models import ProductCart, Product


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart_prod = is_product(pk)

    if cart_prod:
        balance = product.balance - (cart_prod.quantity + 1)
        if balance >= 0:
            cart_prod.quantity += 1
            cart_prod.save()
    else:
        cart = ProductCart()
        cart.product = product
        cart.quantity = 1
        cart.save()

    return redirect('product-list')


def delete_from_cart(request, pk):
    product = is_product(pk)

    if product:
        if product.quantity > 1:
            product.quantity -= 1
            product.save()
        else:
            product.delete()
    return redirect('cart-products-list')


def is_product(pk):
    product = get_object_or_404(Product, id=pk)
    if ProductCart.objects.filter(product=product):
        cart_product = ProductCart.objects.get(product=product)
        return cart_product


class CartListView(ListView):
    template_name = 'cart/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return ProductCart.objects.all()

    def get_sum(self):
        sum = 0
        for products in ProductCart.objects.all():
            sum += products.quantity * products.product.price
        return sum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum'] = self.get_sum()
        return context

