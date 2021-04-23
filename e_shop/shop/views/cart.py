from django.contrib import messages
from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404

from shop.models import Product, Order, OrderProduct
from shop.forms import OrderForm


class AddToCart(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not request.session.get('cart'):
            request.session['cart'] = dict()
        _cart = request.session.get('cart')

        if _cart.get(str(product.id)) is None:
            _cart[str(product.id)] = 1
            messages.add_message(request, messages.SUCCESS, f' {product.product}  добавлен в корзину. Количество: 1шт')
        else:
            balance = product.balance - (_cart.get(str(product.id)) + 1)
            if balance >= 0:
                _cart[str(product.id)] += 1
                messages.add_message(request, messages.SUCCESS, f'{product.product}  добавлен в корзину. Количество: 1шт')
            else:
                messages.add_message(request, messages.ERROR, f'Это был последний {product.product}')

        request.session['cart'] = _cart
        return redirect('shop:product-list')


class DeleteFromCart(View):

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        _cart = request.session.get('cart')
        if _cart.get(str(product.id)):
            if _cart[str(product.id)] > 1:
                _cart[str(product.id)] -= 1
                messages.add_message(request, messages.WARNING, f'{product.product} удален из корзины. Количество: 1шт')
            else:
                del _cart[str(product.id)]
            request.session['cart'] = _cart

        if not _cart:
            return redirect('shop:product-list')
        return redirect('shop:cart-products-list')


class CartListView(ListView):
    template_name = 'cart/list.html'
    context_object_name = 'products'
    form_class = OrderForm
    cart = None
    products = None

    def get(self, request, *args, **kwargs):
        self.cart = request.session.get('cart')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = {}
        for idx, count in self.cart.items():
            product = get_object_or_404(Product, id=int(idx))
            queryset[product] = [count, count*product.price]
        return queryset

    def get_sum(self):
        sum = 0
        self.products = [get_object_or_404(Product, id=int(idx)) for idx in self.cart.keys()]
        for product in self.products:
            sum += self.cart[str(product.id)] * product.price
        return sum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum'] = self.get_sum()
        context['form'] = self.form_class
        context['qty'] = False
        return context


class OrderView(View):
    def post(self, request):
        order = None
        order_form = OrderForm(data=self.request.POST)
        _cart = request.session.get('cart')

        if order_form.is_valid():
            order = Order.objects.create(
                user_name=order_form.cleaned_data.get('user_name'),
                user_phone=order_form.cleaned_data.get('user_phone'),
                user_address=order_form.cleaned_data.get('user_address')
                )

        for idx, qty in _cart.items():
            product = get_object_or_404(Product, id=int(idx))
            OrderProduct.objects.create(products=product, quantity=qty, order=order)
            prod = Product.objects.get(product=product)
            prod.balance -= qty
            prod.save()
            _cart.clear()

        return redirect('shop:product-list')







