from django.db import models


class Style(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['is_deleted', '-created_at']


class Product(models.Model):
    class Category(models.TextChoices):
        MEN = 'MEN', 'Men'
        WOMEN = 'WOMEN', 'Women'
        KIDS = 'KIDS', 'Kids'
        UNISEX = 'UNISEX', 'Unisex'

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    material = models.CharField(max_length=50, null=True, blank=True)
    fit = models.CharField(max_length=50, null=True, blank=True)
    care_instructions = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    category = models.CharField(
        max_length=10, choices=Category.choices, default=Category.UNISEX
    )
    tshirt_type = models.ForeignKey(Style, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
