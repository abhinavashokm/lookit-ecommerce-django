from .models import OrderItems, Review
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Exists, OuterRef, BooleanField, Case, When, Value, Q, F


def reduce_stock_for_order(order_id):
    order_items = OrderItems.objects.filter(order_id=order_id)
    for item in order_items:
        item.variant.stock -= item.quantity
        item.variant.save()


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)

    result = BytesIO()
    pdf = pisa.CreatePDF(src=html, dest=result)

    if pdf.err:
        return None

    return result.getvalue()


def annotate_review_eligibility(user, orders_qs):
    """
    1] A user can give review for a product only once
    2] A user can only review product while it's status is delivered
    """
    reviewed_sq = Review.objects.filter(
        user=user,
        product=OuterRef('variant__product')
    )

    annotated_orders_qs = orders_qs.annotate(
        reviewed=Exists(reviewed_sq)
    ).annotate(
        review_eligible=Case(
            When(
                Q(order_status='DELIVERED') & ~F('reviewed'),
                then=Value(True)
            ),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    return annotated_orders_qs
