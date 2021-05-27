from django.urls import path, include
from rest_framework import routers

from api.views import ProductViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]