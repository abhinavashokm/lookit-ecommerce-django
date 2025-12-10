from django.db import models

# Create your models here.
class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        FLAT = "FLAT", "Flat"
        PERCENTAGE = "PERCENTAGE", "Percentage"
        
    class CouponStatus(models.TextChoices):
        ACTIVE = 'ACTIVE',
        INACTIVE = 'INACTIVE',
        EXPIRED = 'EXPIRED'
  
    code = models.CharField(max_length=50)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.IntegerField()
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    usage_limit = models.IntegerField()
    status = models.CharField(max_length=50, choices=CouponStatus.choices)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)