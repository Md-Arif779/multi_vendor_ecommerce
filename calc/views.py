from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Product, Cart, CartItem, Order, DailyData
from .serializers import (
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    DailyDataSerializer
)

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False)
    def paginate_products(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, 12)  # 12 products per page
        page_number = request.query_params.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj, many=True)
        return Response(serializer.data)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.cartitem_set.all()
        if cart_items.exists():
            order = Order.objects.create(user=user, total_amount=0)
            total_amount = 0
            for cart_item in cart_items:
                order.items.add(cart_item)
                total_amount += cart_item.product.price * cart_item.quantity
            order.total_amount = total_amount
            order.save()
            cart_items.delete()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer
