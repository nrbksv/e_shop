from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404

from shop.models import Product, Order, OrderProduct
from shop.forms import OrderForm


class AddToCart(View):
    def get(self, request, pk):
        qty = int(request.GET.get('qty'))
        if qty > 0:
            product = get_object_or_404(Product, id=pk)

            if not request.session.get('cart'):
                request.session['cart'] = dict()
            _cart = request.session.get('cart')

            if not _cart.get(str(product.id)):
                _cart[str(product.id)] = 0
            balance = product.balance - (_cart.get(str(product.id)) + qty)
            if balance >= 0:
                _cart[str(product.id)] += qty
                messages.add_message(request, messages.SUCCESS, f' "{product.product}"  добавлен в корзину. Количество: {qty}шт')
            else:
                messages.add_message(request, messages.ERROR, f'Выбранное количество превышает осаток на складе "{product.product}"')

            request.session['cart'] = _cart

        redirect_url = 'shop:product-list'
        if request.GET.get('prev'):
            redirect_url = request.GET.get('prev')
        return redirect(redirect_url)


class DeleteFromCart(View):

    def get(self, request, pk, all_):
        product = get_object_or_404(Product, id=pk)
        _cart = request.session.get('cart')

        if all_ == 'True':
            messages.add_message(request, messages.WARNING, f'"{product.product}" удален из корзины.')
            del _cart[str(product.id)]

        if _cart.get(str(product.id)):
            if _cart[str(product.id)] > 1:
                _cart[str(product.id)] -= 1
                messages.add_message(request, messages.WARNING, f'"{product.product}" удален из корзины. Количество: 1шт')
            else:
                messages.add_message(request, messages.WARNING, f'"{product.product}" удален из корзины.')
                del _cart[str(product.id)]

        request.session['cart'] = _cart

        if not _cart:
            return redirect('shop:product-list')

        return redirect('shop:cart-products-list')


class CartListView(ListView):
    template_name = 'cart/list.html'
    context_object_name = 'products'
    form_class = OrderForm
    cart = {}
    products = []

    def get_queryset(self):
        queryset = {}
        self.cart = self.request.session.get('cart', {})
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
            if request.user in get_user_model().objects.all():
                order._user = request.user
            order.save()

        for idx, qty in _cart.items():
            product = get_object_or_404(Product, id=int(idx))
            OrderProduct.objects.create(products=product, quantity=qty, order=order)
            if product.balance - qty >= 0:
                product.balance -= qty
            else:
                order.delete()
                messages.add_message(request, messages.ERROR, f'Произошла ошибка! Количество "{product.product}" на складе {product.balance} шт.')
                return redirect('shop:cart-products-list')
            product.save()
        _cart.clear()
        request.session['cart'] = _cart

        return redirect('shop:product-list')


class UserOrder(LoginRequiredMixin, ListView):
    template_name = 'cart/user_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = {}
        orders = Order.objects.filter(_user=self.request.user.id)
        for order in orders:
            inter = {}
            total_order_sum = 0
            for prod in order.products.all():
                inter[prod] = prod.products.price * prod.quantity
            total_order_sum += sum(inter.values())
            queryset[order] = [inter, total_order_sum]
        return queryset









