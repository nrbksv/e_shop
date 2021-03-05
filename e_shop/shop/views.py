from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product
from shop.forms import ProductForm


def product_list_view(request):
    products = Product.objects.all().order_by('category', 'product')
    return render(request, 'products_list.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_add_view(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_add.html', {'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                category=form.cleaned_data.get('category'),
                product=form.cleaned_data.get('product'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                balance=form.cleaned_data.get('balance')
            )
            return redirect('product-detail', pk=product.id)
        return render(request, 'product_add.html', {'form': form})

