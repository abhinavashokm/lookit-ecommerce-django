from .models import OrderItems, Review
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Exists, OuterRef, BooleanField, Case, When, Value, Prefetch


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
    reviewed_sq = Review.objects.filter(
        user=user,
        product=OuterRef('variant__product')
    )

    items_qs = OrderItems.objects.annotate(
        review_eligible=Exists(reviewed_sq)
    )

    return orders_qs.prefetch_related(
        Prefetch('items', queryset=items_qs)
    )

