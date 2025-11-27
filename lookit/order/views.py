from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import ExpressionWrapper, DecimalField, F, Sum
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from user.models import Address
from .models import Order, OrderItems


@login_required
def checkout(request):
    # ---products in order------------------------------------------------
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

    # ---address list of user, (default address first order)---
    address_list = Address.objects.filter(user=request.user, is_active=True).order_by(
        '-is_default'
    )

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
        {
            "order_items": order_items,
            "price_summary": price_summary,
            "address_list": address_list,
        },
    )


@login_required
@require_POST
def create_order(request):
    user = request.user
    address_id = request.POST.get('address_id')
    address = Address.objects.get(id=address_id, user=user)

    # ---products in order------------------------------------------------
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
    # ---total price of all items in cart considering quantity---------
    sub_total = (
        order_items.aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    tax_amount = sub_total * Decimal(0.05)
    tax_amount = tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    delivery_fee = Decimal(0)
    discount_amount = Decimal(0)
    grand_total = (sub_total + tax_amount + delivery_fee) - discount_amount
    
    order = None
    try:
        with transaction.atomic():

            order = Order.objects.create(
                user=user,
                address=address,
                sub_total=sub_total,
                delivery_fee=delivery_fee,
                discount_amount=discount_amount,
                tax_amount=tax_amount,
                total_amount=grand_total,
            )
            for item in order_items:
                OrderItems.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    unit_price=item.variant.product.price,
                    sub_total=item.sub_total_per_product,
                )
            #imp: need to delete cart

    except Exception as e:
        messages.error(request, e)
        print(e)
        return redirect('checkout')

    return redirect('payment-page',order_id = order.id)


def payment_page(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "order/payment.html/", {"order":order})