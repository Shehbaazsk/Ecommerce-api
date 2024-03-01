from django.db import models
from users.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    class PaymentStatus:
        SUCCESS = 'success'
        FAILED = 'failed'
        PENDING = 'pending'
        choices=[
            (SUCCESS,'success'),
            (FAILED,'failed'),
            (PENDING,'pending')
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    is_ordered = models.BooleanField(default=False)
    address = models.TextField()
    payment_status = models.CharField(max_length=10,choices=PaymentStatus.choices,default='pending')
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    signature_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}-{self.user}-{self.payment_status}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.product.price
        return super().save(*args, **kwargs)
    





