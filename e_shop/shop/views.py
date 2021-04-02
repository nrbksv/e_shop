from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import reverse

from shop.models import Product, Category
from shop.forms import ProductForm, SearchForm


class ProductListView(ListView):
    template_name = 'products_list.html'
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
    template_name = 'product_detail.html'
    model = Product


class ProductCreateView(CreateView):
    template_name = 'product_add.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.kwargs.get('pk')})


class ProductDeleteView(DeleteView):
    template_name = 'delete_confirm.html'
    model = Product
    success_url = reverse_lazy('product-list')
