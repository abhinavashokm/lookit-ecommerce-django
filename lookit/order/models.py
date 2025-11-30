from django.db import models
from user.models import User, Address
from product.models import Variant
import uuid
from django.utils import timezone


class Order(models.Model):
    
    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        CREDIT_CARD = 'CREDIT', 'Credit Card'
        DEBIT_CARD = 'DEBIT', 'Debit Card'
        UPI = 'UPI', 'UPI'
        WALLET = 'WALLET', 'Wallet'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, blank=True)
    
    total_items = models.PositiveIntegerField(default=0)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2) #sum of base price of all items
    discount_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_total = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class OrderItems(models.Model):
    
    class OrderStatus(models.TextChoices):
        INITIATED = 'INITIATED', 'Order Initiated'
        PLACED = 'PLACED', 'Order Placed'
        SHIPPED = 'SHIPPED', 'Shipped'
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Out For Delivery'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
        RETURNED = 'RETURNED', 'Returned'
        
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        COD = 'COD', 'Cash on Delivery'
        REFUNDED = 'REFUNDED', 'Refunded'
        
    order_item_id = models.CharField(max_length=20, blank=True, null=True) # add unique True
        
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) #base price without tax
    sub_total = models.DecimalField(max_digits=10, decimal_places=2) #quantity x unit_price
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # final line total
    
    order_status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.INITIATED)
    cancel_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    placed_at = models.DateTimeField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    out_for_delivery_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def product(self):
        return self.variant.product
    
    def save(self, *args, **kwargs):
        if not self.order_item_id:
            # Example: ORD-2025-000123
            year = timezone.now().year
            prefix = "ORD"
            # Pad database ID estimate — better to use random unique portion before first save
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.order_item_id = f"{prefix}-{year}-{unique_num}"
        super().save(*args, **kwargs)
