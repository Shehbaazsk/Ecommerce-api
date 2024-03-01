from django.urls import path
from carts.api.api_views import get_cart, add_to_cart, update_cart, delete_cart, clear_cart

app_name = "carts"

urlpatterns = [
    path('get_cart/',get_cart,name='cart'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('update_cart/',update_cart,name='update_cart'),
    path('delete_cart/<int:product_id>',delete_cart,name='delete_cart'),
    path('clear_cart/',clear_cart,name='clear_cart')
]
