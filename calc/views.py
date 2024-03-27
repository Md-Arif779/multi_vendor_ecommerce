from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order, DailyData
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, DailyDataSerializer
# Create your views here.




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        cart_items = request.user.cart.cartitem_set.all()
        if cart_items.exists():
            order = Order.objects.create(user=request.user, total_amount=0)  # Initialize order
            total_amount = 0
            for cart_item in cart_items:
                order.items.add(cart_item)
                total_amount += cart_item.product.price * cart_item.quantity
            order.total_amount = total_amount
            order.save()
            request.user.cart.cartitem_set.all().delete()  # Empty the cart
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer
