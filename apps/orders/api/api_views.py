from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart
from orders.serializers import OrderSerializer,OrderItemSerializer
from orders.models import Order, OrderItem
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def order_listing(request):
    """"Funciton to listing order which is paid"""

    data=[]
    orders = Order.objects.filter(user=request.user,is_ordered=True)
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_data = OrderSerializer(order).data
        order_item_data = OrderItemSerializer(items,many=True)
        order_data['order_items'] = order_item_data
        data.append(order_data)
    return Response({'data':data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_order(request):
    """"Checkout cart item to order"""

    if not request.data.get('cart_id'):
        raise ValueError("Cart id is required")
    cart_id = request.data.get('cart_id')
    
    cart = get_object_or_404(Cart,id=cart_id,user=request.user)
    cart_items = cart.cart_items.all()
    with transaction.atomic():
        user_order = Order.objects.create(user=request.user)
        objs = [OrderItem(order=user_order,product=item.product,quantity=item.quantity,amount=item.product.price*item.quantity) \
                for item in cart_items]
        order_items = OrderItem.objects.bulk_create(objs)
        total_amount = 0
        for item in cart_items:
            total_amount += item.product.price
        user_order.total_amount = total_amount
        user_order.address = request.user.address
        user_order.save()
        cart_items.delete()
    order_data = OrderSerializer(user_order).data
    order_items_data = OrderItemSerializer(order_items,many=True).data
    order_data['order_item'] = order_items_data
    return Response(order_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_payment(request):
    """"Payment integration for the order"""

    if not request.data['order_id']:
        raise ValueError("order id is required")
    order_id = request.data['order_id']
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    amount = get_object_or_404(Order,pk=order_id).total_amount
    try:
        payment = client.order.create({'amount':int(amount)*100,'currency':'INR','payment_capture':'1','receipt':order_id})
        return Response(payment,status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def payment_callback(request):
    """"Callback function to check whether payment is received or not"""

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    response = request.data.dict()
    order_id=request.data['order_id']
    if 'razorpay_signature' in response:
        data = client.utility.verify_payment_signature(response)
        if data:
            order = Order.objects.get(pk=order_id)
            order.is_ordered=True
            order.payment_status=Order.PaymentStatus.SUCCESS
            order.payment_id = response['razorpay_payment_id']
            order.signature_id = response['razorpay_signature']
            order.save()
            return Response({'status': 'Payment Done'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Signature Mismatch!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        error_code = response['error[code]']
        error_source = response['error[source]']
        error_reason = response['error[reason]']
        error_data = {
                'error_code': error_code,
                'error_source': error_source,
                'error_reason': error_reason,
            }
        return Response({'error_data': error_data}, status=status.HTTP_401_UNAUTHORIZED)