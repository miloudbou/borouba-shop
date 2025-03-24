from rest_framework import serializers
from .models import Product, Category, Order, OrderItem, Cart, CartItem, GuestOrder

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'price', 'currency', 'image_url', 'affiliate_link', 'aliexpress_product_id', 'created_at']
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'status', 'items']

class GuestOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestOrder
        fields = ['id', 'name', 'email', 'address', 'created_at', 'total_price', 'status']

