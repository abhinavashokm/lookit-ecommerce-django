from product.models import Product, Style
from order.models import OrderItems
from offer.models import Offer
from user.models import User
from offer.utiils import annotate_offer_status
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
from django.db.models import Sum, DecimalField
from django.db.models.functions import (
    Coalesce,
    ExtractMonth,
    ExtractYear,
    ExtractWeek,
    TruncDate,
    ExtractDay,
    Ceil,
)
from datetime import date, timedelta
from django.utils import timezone

today = date.today()

# Last 7 days (excluding today)
last_7_days = today - timedelta(days=7)

# Month to date (start of this month)
month_to_date = today.replace(day=1)

# Year to date (start of this year)
year_to_date = today.replace(month=1, day=1)


def get_start_date_for_filter(filter):
    start_date = None
    if filter == 'week':
        start_date = last_7_days
    elif filter == 'month':
        start_date = month_to_date
    elif filter == 'year':
        start_date = year_to_date
    else:
        return None
    return start_date


def get_top_selling_products(filter):
    """function to return top selling 10 products of given time period"""
    start_date = get_start_date_for_filter(filter)
    top_sellers = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED,
            variant__orders__placed_at__date__gte=start_date,
        )
        .annotate(
            units_sold=Count('variant__orders'),
        )
        .annotate(total_revenue=Sum('variant__orders__total'))
        .order_by('-units_sold')[:10]
    )

    return top_sellers


def get_top_selling_styles(filter):
    # fetch top 10 sold styles
    start_date = get_start_date_for_filter(filter)
    top_selling_styles = (
        Style.objects.filter(
            product__variant__orders__order_status=OrderItems.OrderStatus.DELIVERED,
            product__variant__orders__placed_at__date__gte=start_date,
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

    return top_selling_styles


def get_top_selling_brands(filter):
    start_date = get_start_date_for_filter(filter)
    top_selling_brands = (
        Product.objects.filter(
            variant__orders__order_status=OrderItems.OrderStatus.DELIVERED,
            variant__orders__placed_at__date__gte=start_date,
        )
        .values('brand')
        .annotate(
            sale_count=Coalesce(
                Count('variant__orders'), Value(0), output_field=IntegerField()
            )
        )
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


def get_dashboard_summary(filter):
    summary = {}

    order_summary = OrderItems.objects.filter(
        order_status=OrderItems.OrderStatus.DELIVERED
    ).aggregate(
        total_sales=Coalesce(
            Sum('total'),
            Value(0),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
        total_orders=Count('id'),
    )

    offer_set = Offer.objects.all()
    status_annotated_offers = annotate_offer_status(offer_set)

    summary['total_sales'] = order_summary.get('total_sales')
    summary['total_orders'] = order_summary.get('total_orders')
    summary['active_offers'] = status_annotated_offers.filter(status='active').count()
    summary['users_count'] = User.objects.all().count()

    return summary



def get_sales_performance(filter):
    start_date = get_start_date_for_filter(filter)

    data_values = None
    data_labels = None
    
    if filter == 'year':
        sales_performance = (
            OrderItems.objects.filter(
                order_status=OrderItems.OrderStatus.DELIVERED,
                placed_at__date__gte=start_date,
            )
            .annotate(
                month=ExtractMonth('placed_at'),
                year=ExtractYear('placed_at'),
            )
            .values('month')
            .annotate(
                total_sales=Coalesce(
                    Sum('total'),
                    0,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .order_by('month')
        )
        data_values = [0] * 12
        data_labels = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
        ]
        for record in sales_performance:
            # print(f"{record['month']:02d}-{record['year']}: ₹{record['total_sales']}")
            data_values[record['month'] - 1] = float(record['total_sales'])
            
    elif filter == 'month':
        
        sales_performance = (
            OrderItems.objects.filter(
                order_status=OrderItems.OrderStatus.DELIVERED,
                placed_at__date__gte=start_date,
            )
            .annotate(
                week_of_month=ExpressionWrapper(
                    Ceil(ExtractDay('placed_at') / 7.0),
                    output_field=IntegerField(),
                ),
            )
            .values('week_of_month')
            .annotate(
                total_sales=Coalesce(
                    Sum('total'),
                    0,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .order_by('week_of_month')
        )
        
        data_values = [0] * 4
        data_labels = [
            'Week-1',
            'Week-2',
            'Week-3',
            'Week-4',
        ]
        for record in sales_performance:
            # print(f"{record['month']:02d}-{record['year']}: ₹{record['total_sales']}")
            data_values[record['week_of_month'] - 1] = float(record['total_sales'])
            
    elif filter == 'week':
        last_7_days_sales = (
            OrderItems.objects.filter(
                order_status=OrderItems.OrderStatus.DELIVERED,
                placed_at__date__lt=today,
                placed_at__date__gte=today - timezone.timedelta(days=7),
            )
            .annotate(
                day=TruncDate('placed_at'),
                day_number=ExpressionWrapper(
                    today - TruncDate('placed_at'),
                    output_field=IntegerField(),
                ),
            )
            .values('day', 'day_number')
            .annotate(
                total_sales=Coalesce(
                    Sum('total'),
                    0,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .order_by('day_number')
        )
        data_values = [0] * 7
        data_labels = [
            'Day-1',
            'Day-2',
            'Day-3',
            'Day-4',
            'Day-5',
            'Day-6',
            'Day-7',
        ]
        # for record in last_7_days_sales:
            # print(f"{record['month']:02d}-{record['year']}: ₹{record['total_sales']}")
            # data_values[record['day_number'] - 1] = float(record['total_sales'])
            
    
    return {"data_values":data_values, "data_labels":data_labels}