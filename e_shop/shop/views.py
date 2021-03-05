from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product


def product_list_view(request):
    products = Product.objects.all().order_by('category', 'product')
    return render(request, 'products_list.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})

