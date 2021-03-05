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

from shop.views import product_list_view, product_detail_view, product_add_view, product_update_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_list_view, name='product-list'),
    path('product/<int:pk>', product_detail_view, name='product-detail'),
    path('product/add', product_add_view, name='product-add'),
    path('product/<int:pk>/update', product_update_view, name='product-update'),

]
