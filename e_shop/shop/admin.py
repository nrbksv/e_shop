from django.contrib import admin


from shop.models import Product


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'product', 'price', 'balance']
    list_filter = ['category']
    search_fields = ['product', 'category']
    fields = ['id', 'category', 'product', 'description', 'price', 'balance']
    readonly_fields = ['id']


admin.site.register(Product, ShopAdmin)
