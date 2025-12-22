from product.models import Product, Style
from order.models import OrderItems
from django.db.models import (
    Count,
    Sum,
    DecimalField,
    F,
    ExpressionWrapper,
    IntegerField,
    Value,
)
from django.db.models.functions import Coalesce


def get_top_selling_products():
    """function to return top selling 10 products of given time period"""
    top_sellers = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED
        )
        .annotate(
            units_sold=Count('variant__orders'),
        )
        .annotate(total_revenue=Sum('variant__orders__total'))
        .order_by('-units_sold')[:10]
    )

    return top_sellers


def get_top_selling_styles():
    # fetch top 10 sold styles
    top_selling_styles = (
        Style.objects.filter(
            product__variant__orders__order_status=OrderItems.OrderStatus.DELIVERED
        )
        .annotate(sale_count=Count('product__variant__orders'))
        .annotate(
            total_sales=Coalesce(
                Sum('product__variant__orders__total'),
                0,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        .order_by('-total_sales')[:10]
    )

    # Avoid errors if queryset empty
    if not top_selling_styles:
        return []

    # Use the highest total as 100%
    base_for_calculation = (
        top_selling_styles[0].sale_count or 1
    )  # prevent divide by zero

    # annotate percentage for each style (for graph representation)
    top_selling_styles = top_selling_styles.annotate(
        sale_percentage=ExpressionWrapper(
            F('sale_count') * 100 / base_for_calculation, output_field=IntegerField()
        )
    )

    for i in top_selling_styles:
        print(i.sale_percentage)

    return top_selling_styles


def get_top_selling_brands():
    top_selling_brands = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED
        )
        .values('brand')
        .annotate(sale_count=Coalesce(Count('variant__orders'), Value(0), output_field=IntegerField() ))
        .order_by('-sale_count')
    )

    # Avoid errors if queryset empty
    if not top_selling_brands:
        return []

    # Use the highest total as 100%
    base_for_calculation = (
        top_selling_brands[0].get('sale_count') or 1
    )  # prevent divide by zero
    
    # annotate percentage for each style (for graph representation)
    top_selling_brands = top_selling_brands.annotate(
        sale_percentage=ExpressionWrapper(
            F('sale_count') * 100 / base_for_calculation, output_field=IntegerField()
        )
    )

    return top_selling_brands
