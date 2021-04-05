from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404

from shop.models import ProductCart, Product, Order, OrderProduct
from shop.forms import OrderForm


class AddToCart(View):
    def get(self, _, pk):
        product = get_object_or_404(Product, id=pk)
        cart_prod = ProductCart.objects.filter(product=product)

        if cart_prod:
            cart_prod = ProductCart.objects.get(product=product)
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


class DeleteFromCart(View):

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart_product = ProductCart.objects.get(product=product)

        if cart_product:
            if cart_product.quantity > 1:
                cart_product.quantity -= 1
                cart_product.save()
            else:
                cart_product.delete()
        return redirect('cart-products-list')


class CartListView(ListView):
    template_name = 'cart/list.html'
    context_object_name = 'products'
    form_class = OrderForm

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
        context['form'] = self.form_class
        return context


class OrderView(View):
    def post(self, request):
        order = None
        order_form = OrderForm(data=self.request.POST)
        if order_form.is_valid():
            order = Order.objects.create(
                user_name=order_form.cleaned_data.get('user_name'),
                user_phone=order_form.cleaned_data.get('user_phone'),
                user_address=order_form.cleaned_data.get('user_address')
                )
        for product in ProductCart.objects.all():
            OrderProduct.objects.create(products=product.product, quantity=product.quantity, order=order)
            ProductCart.objects.all().delete()
        return redirect('product-list')







