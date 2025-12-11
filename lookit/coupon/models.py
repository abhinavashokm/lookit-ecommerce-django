from django.db import models


# Create your models here.
class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        FLAT = "FLAT", "Flat"
        PERCENTAGE = "PERCENTAGE", "Percentage"

    class CouponStatus(models.TextChoices):
        ACTIVE = ('ACTIVE',)
        INACTIVE = ('INACTIVE',)
        EXPIRED = 'EXPIRED'
        LIMIT_REACHED = 'LIMIT_REACHED', 'Usage Limit Reached'

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.IntegerField()
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    usage_limit = models.IntegerField()
    usage_remaining = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=CouponStatus.choices)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Only when instance is newly created (no ID yet)
        if not self.pk and not self.usage_remaining:
            self.usage_remaining = self.usage_limit  # set based on another field
        super().save(*args, **kwargs)
