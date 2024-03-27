
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet, DailyDataViewSet



from .views import ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet, DailyDataViewSet



router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

router.register(r'daily-data', DailyDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderViewSet.as_view({'post': 'create'}), name='order-create'), 
]
