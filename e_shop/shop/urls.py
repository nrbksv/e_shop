from django.urls import path

from shop.views import (
        ProductListView,
        ProductDetailView,
        ProductCreateView,
        ProductUpdateView,
        ProductDeleteView,
        AddToCart,
        CartListView,
        DeleteFromCart,
        OrderView,
        UserOrder,
    )


app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('add', ProductCreateView.as_view(), name='product-add'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/add/cart', AddToCart.as_view(), name='add-to-cart'),
    path('cart/products', CartListView.as_view(), name='cart-products-list'),
    path('cart/product/<int:pk><str:all_>/delete', DeleteFromCart.as_view(), name='cart-product-delete'),
    path('cart/order', OrderView.as_view(), name='order'),
    path('user/order', UserOrder.as_view(), name='user-order'),
]