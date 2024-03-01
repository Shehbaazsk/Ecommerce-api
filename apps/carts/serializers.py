from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','price']

class CartItemSerializers(serializers.ModelSerializer):
    product = CartProductSerializers()
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializers(serializers.ModelSerializer):
    cart_items = CartItemSerializers(many=True)
    class Meta:
        model = Cart
        fields = ['id','user','cart_items']


