from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'
    USER_TYPE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=BUYER)

    # Add unique related_name arguments to resolve clashes
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='calc_user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='calc_user_permissions')


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.pk} - User: {self.user.username}, Created At: {self.created_at}"
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart Item - Cart: {self.cart}, Product: {self.product}, Quantity: {self.quantity}"
        

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order #{self.pk} - User: {self.user.username}, Total Amount: {self.total_amount}, Created At: {self.created_at}"

class DailyData(models.Model):
    date = models.DateField(unique=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Date: {self.date}, Total Sales: {self.total_sales}"
