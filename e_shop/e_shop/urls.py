"""e_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from accounts.views import UserRegisterView
from shop.views import (
        ProductListView,
        ProductDetailView,
        ProductCreateView,
        ProductUpdateView,
        ProductDeleteView,
        AddToCart,
        CartListView,
        DeleteFromCart,
        OrderView
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('product/add', ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('product/<int:pk>/add/cart', AddToCart.as_view(), name='add-to-cart'),
    path('cart/products', CartListView.as_view(), name='cart-products-list'),
    path('cart/product/<int:pk>/delete', DeleteFromCart.as_view(), name='card-product-delete'),
    path('cart/order', OrderView.as_view(), name='order'),
    path('register/', UserRegisterView.as_view(), name='user-register')
]