from django.urls import path
from orders.api.api_views import checkout_order,order_payment,payment_callback,order_listing

app_name = 'orders'

urlpatterns = [
    path("order_listing/",order_listing, name="order_listing"),
    path('checkout_order/',checkout_order,name='checkout_order'),
    path('order_payment',order_payment,name='order_payment'),
    path('payment_callback/',payment_callback,name='payment_callback')
]
