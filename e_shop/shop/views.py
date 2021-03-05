from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product


def product_list_view(request):
    products = Product.objects.all().order_by('category', 'product')
    return render(request, 'products_list.html', {'products': products})




