from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product
from shop.forms import ProductForm


def product_list_view(request):
    products = Product.objects.all().order_by('category', 'product')
    return render(request, 'products_list.html', {'products': products, 'categories': Product.CATEGORY_CHOICES})


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


def product_update_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'GET':
        form = ProductForm(initial={
            'category': product.category,
            'product': product.product,
            'description': product.description,
            'price': product.price,
            'balance': product.balance
        })
        return render(request, 'product_update.html', {'form': form, 'product': product})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.category = form.cleaned_data.get('category')
            product.product = form.cleaned_data.get('product')
            product.description = form.cleaned_data.get('description')
            product.price = form.cleaned_data.get('price')
            product.balance = form.cleaned_data.get('balance')
            product.save()
            return redirect('product-detail', pk=product.id)
        return render(request, 'product_update.html', {'form': form, 'product': product})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'GET':
        return render(request, 'delete_confirm.html', {'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('product-list')


def filter_view(request, category):
    products = Product.objects.filter(category=category).order_by('product')
    return render(request, 'products_list.html', {'products': products, 'categories': Product.CATEGORY_CHOICES})
