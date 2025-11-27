from django.db import models
from user.models import User, Address
from product.models import Variant

class Order(models.Model):
    
    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        CREDIT_CARD = 'CREDIT', 'Credit Card'
        DEBIT_CARD = 'DEBIT', 'Debit Card'
        UPI = 'UPI', 'UPI'
        WALLET = 'WALLET', 'Wallet'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        COD = 'COD', 'Cash on Delivery'
        REFUNDED = 'REFUNDED', 'Refunded'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, blank=True)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class OrderItems(models.Model):
    
    class OrderStatus(models.TextChoices):
        PLACED = 'PLACED', 'Order Placed'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
        RETURNED = 'RETURNED', 'Returned'
        
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    cancel_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)