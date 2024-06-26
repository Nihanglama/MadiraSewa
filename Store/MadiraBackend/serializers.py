from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Products,Cart,Order,Shipping

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']

class CartSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'get_total_amount']

class OrderSerializer(ModelSerializer):
    cart_set = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date', 'status', 'transaction_id', 'get_total_products', 'get_total_amount', 'cart_set']

class ShippingSerializer(ModelSerializer):
    class Meta:
        model=Shipping
        fields=["address","phone","email","city","state"]
