from django.contrib import admin

from shop.models import Product, Category, Order, OrderProduct


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'product', 'price', 'balance']
    list_filter = ['category']
    search_fields = ['product', 'category']
    fields = ['id', 'category', 'product', 'description', 'price', 'balance']
    readonly_fields = ['id']


admin.site.register(Product, ShopAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
    fields = ['id', 'category']
    readonly_fields = ['id']


admin.site.register(Category, CategoryAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', '_user', 'user_name', 'user_phone', 'user_address', 'created_at']
    fields = ['id', '_user', 'user_name', 'user_phone', 'user_address', 'created_at']
    readonly_fields = ['id', 'created_at']


admin.site.register(Order, OrderAdmin)


class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity']
    fields = ['id', 'products', 'quantity', 'order']
    readonly_fields = ['id']


admin.site.register(OrderProduct, OrderProductsAdmin)