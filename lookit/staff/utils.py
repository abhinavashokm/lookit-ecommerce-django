from product.models import Product
from order.models import OrderItems
from django.db.models import Count, Sum


def get_top_selling_products():
    """function to return top selling 10 products of given time period"""
    top_sellers = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED
        )
        .annotate(
            units_sold=Count('variant__orders'),
        )
        .annotate(
            total_revenue = Sum('variant__orders__total')
        )
        .order_by('-units_sold')[:10]
    )

    return top_sellers
