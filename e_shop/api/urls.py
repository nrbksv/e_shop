from django.urls import path, include
from rest_framework import routers

from api.views import ProductViewSet, OrderViewSet, Cart, get_token_view

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', Cart.as_view(), name='cart-list'),
    path('csrf/', get_token_view, name='csrf')
]