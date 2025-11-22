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
    brand = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    image_url = models.URLField()

    material = models.CharField(max_length=50, null=True, blank=True)
    fit = models.CharField(max_length=50, null=True, blank=True)
    care_instructions = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    category = models.CharField(
        max_length=10, choices=Category.choices, default=Category.UNISEX
    )
    style = models.ForeignKey(Style, on_delete=models.PROTECT, blank=True, null=True)
    base_color = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_active','-created_at']
        
        
class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.CharField(max_length=10)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'size'], name="unique_product_size")
        ]
    
    #ensure size is always upper case
    def save(self, *args, **kwargs):
        if self.size:
            self.size = self.size.upper()
        super().save(*args, **kwargs)
