from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import reverse

from shop.models import Product, Category
from shop.forms import ProductForm, SearchForm


class ProductListView(ListView):
    template_name = 'products/list.html'
    context_object_name = 'products'
    model = Product
    search_form = SearchForm()
    ordering = '-category', 'product'
    paginate_by = 10
    category = None
    search_item = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['categories'] = Category.objects.all()
        if self.search_item:
            context['query'] = urlencode({'search': self.search_item})
        if self.request.session.get('cart'):
            qty = 0
            for key, value in self.request.session.get('cart').items():
                qty += value
            context['qty'] = qty
        return context

    def get(self, request, **kwargs):
        self.category = request.GET.get('product/category')
        self.search_item = request.GET.get('search')
        return super().get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(balance__gt=0)
        if self.search_item:
            queryset = queryset.filter(product__contains=self.search_item)
        if self.category:
            queryset = queryset.filter(category=self.category)
        return queryset


class ProductDetailView(DetailView):
    template_name = 'products/detail.html'
    model = Product


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'products/add.html'
    model = Product
    form_class = ProductForm
    permission_required = 'add_product'

    def has_permission(self):
        return self.request.user.groups.filter(name='Модераторы') or super().has_permission()

    def get_success_url(self):
        return reverse('shop:product-detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'products/update.html'
    model = Product
    form_class = ProductForm
    permission_required = 'change_product'

    def has_permission(self):
        return self.request.user.groups.filter(name='Модераторы') or super().has_permission()

    def get_success_url(self):
        return reverse('shop:product-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'products/delete.html'
    model = Product
    success_url = reverse_lazy('shop:product-list')
    permission_required = 'delete_product'

    def has_permission(self):
        return self.request.user.groups.filter(name='Модераторы') or super().has_permission()
