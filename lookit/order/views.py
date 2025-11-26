from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from user.models import Address
from django.db.models import ExpressionWrapper, DecimalField, F, Sum
from decimal import Decimal, ROUND_HALF_UP


@login_required
def checkout(request):
    #---products in order------------------------------------------------
    order_items = (
        Cart.objects.filter(user=request.user)
        .select_related('variant')
        .annotate(
            sub_total_per_product=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )
    
    #---address list of user---
    address_list = Address.objects.filter(user=request.user)

    # ---total price of all items in cart considering quantity---------
    sub_total = (
        order_items.aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    tax = sub_total * Decimal(0.05)
    # ROUND_HALF_UP -> ROUNDING METHOD USED - less than 0.5 then reduce, greater than or equal to 0.5 then increase(BANKERS STYLE)
    tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    price_summary = {"sub_total": sub_total, "tax": tax, "grand_total": sub_total + tax}

    return render(
        request,
        "order/checkout.html",
        {"order_items": order_items, "price_summary": price_summary, "address_list":address_list},
    )
