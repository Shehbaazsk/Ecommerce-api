from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from carts.models import Cart, CartItem
from carts.serializers import CartSerializers
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def get_cart(request):
    """"Get Cart Detail Function"""

    user = request.user
    cart,created = Cart.objects.get_or_create(user=user)
    return Response(CartSerializers(cart).data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, *args, **kwargs):
    """Function to add product into cart """

    user = request.user
    cart,created = Cart.objects.get_or_create(user=user)
    if not request.data['product_id']:
        raise ValueError("Product id is required")
    product = Product.objects.get(pk=request.data['product_id'])
    quantity = request.data.get('quantity',1)
    cart_item = CartItem.objects.filter(cart=cart,product=product).first()
    with transaction.atomic():
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart,product=product,quantity=quantity)
    return Response({"message" : "Item added to cart"},status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    """"Function to update product quantity in cart"""

    user = request.user
    cart = get_object_or_404(Cart,user=user)
    if not request.data['product_id']:
        raise ValueError("Product id is required")
    if not request.data['quantity']:
        raise ValueError("Quantity is required")
    product_id = request.data['product_id']
    quantity = request.data['quantity'] 
    cart_item = CartItem.objects.filter(cart=cart,product=product_id).first()
    cart_item.quantity = quantity
    cart_item.save()
    return Response({'messgae':'Cart updated'}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request,product_id):
    """Function to delete item/product from cart"""

    cart_item = get_object_or_404(CartItem,product=product_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
        return Response({'message':"Item Deleted"},status=status.HTTP_204_NO_CONTENT)
    return Response({'message': "Item not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """"Function to clear all prodcut from the cart"""

    CartItem.objects.filter(cart__user=request.user).delete()
    return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)