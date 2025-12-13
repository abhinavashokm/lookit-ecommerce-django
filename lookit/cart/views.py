from django.shortcuts import render, redirect
from .models import Cart, CartAppliedCoupon
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Sum,
    F,
    ExpressionWrapper,
    DecimalField,
    Case,
    When,
    Value,
    BooleanField,
    OuterRef,
    Subquery,
    Max,
    IntegerField,
)
from django.db.models.functions import Coalesce, Greatest, Round
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db import transaction
from product.models import Variant
from coupon.utils import is_valid_coupon
from coupon.models import Coupon
from offer.models import Offer


@login_required
def cart(request):

    # sub queries for fetching offers
    product_discount_sq = (
        Offer.objects.filter(products=OuterRef('variant__product__id'))
        .values('products')
        .annotate(max_discount=Max('discount'))
        .values('max_discount')[:1]
    )

    category_discount_sq = (
        Offer.objects.filter(style=OuterRef('variant__product__style'))
        .values('style')
        .annotate(max_discount=Max('discount'))
        .values('max_discount')[:1]
    )

    cart_items = (
        Cart.objects.filter(user=request.user)
        .select_related('variant')
        .annotate(
            sub_total_per_product=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            stock_available=Case(
                When(variant__stock__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            is_product_active=F('variant__product__is_active'),
        )
        .order_by('-stock_available', '-is_product_active')
        .annotate(
            product_discount=Coalesce(
                Subquery(product_discount_sq), Value(0), output_field=IntegerField()
            ),
            category_discount=Coalesce(
                Subquery(category_discount_sq), Value(0), output_field=IntegerField()
            ),
        )
        .annotate(
            offer_percentage=Greatest(F('product_discount'), F('category_discount'))
        )
        .annotate(
            discount_amount=ExpressionWrapper(
                Round(
                    (F('variant__product__price') * F('offer_percentage') / Value(100)),
                    2,
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        .annotate(
            offer_price=ExpressionWrapper(
                (F('variant__product__price') - F('discount_amount')),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )
    # cart price summary
    sub_total = (
        cart_items.filter(is_product_active=True, stock_available=True).aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    
    total_discount_amount = cart_items.aggregate(total = Sum('discount_amount'))['total']
    
    tax = sub_total * Decimal(0.05)
    # ROUND_HALF_UP -> ROUNDING METHOD USED - less than 0.5 then reduce, greater than or equal to 0.5 then increase(BANKERS STYLE)
    tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    cart_summary = {"sub_total": sub_total, "tax": tax, "offer_discount": total_discount_amount, "grand_total": sub_total - total_discount_amount}

    # --for disabling checkout button if a product is unavailable or out of stock
    checkout_block = False
    for item in cart_items:
        if not item.stock_available or not item.is_product_active:
            checkout_block = True
            break

    # --fetch all saved coupons by user
    user = request.user
    saved_coupons = user.saved_coupons.all()

    # --fetch applied coupon----------------
    applied_coupon = None
    cart_applied_exist = CartAppliedCoupon.objects.filter(user=request.user).first()
    if cart_applied_exist:
        applied_coupon = cart_applied_exist.coupon
        if applied_coupon.discount_type == 'FLAT':
            cart_summary['coupon_discount'] = applied_coupon.discount_value
        elif applied_coupon.discount_type == 'PERCENTAGE':
            cart_summary['coupon_discount'] = (
                cart_summary['grand_total'] * applied_coupon.discount_value
            ) / 100
        cart_summary['grand_total'] -= cart_summary['coupon_discount']

    return render(
        request,
        'cart/cart.html',
        {
            "cart_items": cart_items,
            "cart_summary": cart_summary,
            "checkout_block": checkout_block,
            "saved_coupons": saved_coupons,
            "applied_coupon": applied_coupon,
        },
    )


@login_required
def remove_cart_item(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        try:
            Cart.objects.get(variant_id=variant_id).delete()
            messages.success(request, "ITEM REMOVED FROM CART")
        except Exception as e:
            messages.error(request, e)

    return redirect('cart')


@login_required
def update_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)

        cart_id = data.get('cart_id')
        variant_id = data.get('variant_id')
        new_quantity = data.get('new_quantity')

        try:
            with transaction.atomic():
                cart_item = Cart.objects.get(id=cart_id, variant_id=variant_id)
                product_variant = Variant.objects.get(id=variant_id)

                old_quantity = cart_item.quantity
                cart_item.quantity = new_quantity
                quantity_change = new_quantity - old_quantity

                if quantity_change > 0:
                    if product_variant.stock < new_quantity:
                        return JsonResponse(
                            {
                                "error": "Stock not available",
                                "quantity": old_quantity,
                            }
                        )

                product_variant.save()
                cart_item.save()
        except Exception as e:
            print("ERROR: ", e)
            messages.error(request, "Something went wrong!")

    # ---fetch updated cart summary----
    cart_items = (
        Cart.objects.filter(user=request.user)
        .select_related('variant')
        .annotate(
            sub_total_per_product=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            stock_available=Case(
                When(variant__stock__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            is_product_active=F('variant__product__is_active'),
            unit_price=F('variant__product__price'),
        )
    )
    # cart price summary
    sub_total = (
        cart_items.filter(is_product_active=True, stock_available=True).aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    tax = sub_total * Decimal(0.05)
    # ROUND_HALF_UP -> ROUNDING METHOD USED - less than 0.5 then reduce, greater than or equal to 0.5 then increase(BANKERS STYLE)
    tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    cart_summary = {"sub_total": sub_total, "tax": tax, "grand_total": sub_total + tax}

    cart_items = list(
        cart_items.values('id', 'quantity', 'unit_price', 'sub_total_per_product')
    )

    return JsonResponse(
        {
            "status": "success",
            "message": "Quantity updated",
            "new_quantity": new_quantity,
            "cart_summary": cart_summary,
            "cart_items": cart_items,
        }
    )


@login_required
def save_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        # --check validity-------------------------
        valid_coupon = is_valid_coupon(coupon_code)

        if valid_coupon:
            coupon = Coupon.objects.get(code=coupon_code)
            request.user.saved_coupons.add(coupon)
            messages.success(request, 'New Coupon Saved Successfully')
        else:
            messages.error(request, "Invalid coupon code!")

    return redirect('cart')


@login_required
def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')

        # --check if user already applied another coupon
        applied_coupon_exist = CartAppliedCoupon.objects.filter(
            user=request.user
        ).exists()
        if applied_coupon_exist:
            messages.error(request, "Only one coupon can be applied at a time")
            return redirect('cart')

        # --check validity-------------------------
        valid_coupon = is_valid_coupon(coupon_code)

        if valid_coupon:
            coupon = Coupon.objects.get(code=coupon_code)

            # --add coupon to users cart-------------------
            try:
                CartAppliedCoupon.objects.create(user=request.user, coupon=coupon)
                messages.success(request, 'Coupon Applied Successfully')
            except Exception as e:
                print("Error: ", e)
                messages.error(request, "Something went wrong!")

        else:
            messages.error(request, "Coupon Limit Expired!")

    return redirect('cart')


@login_required
def remove_coupon(request):
    if request.method == 'POST':
        # --remove applied coupon of the user-----------------------
        try:
            CartAppliedCoupon.objects.filter(user=request.user).delete()
            messages.success(request, "Applied coupon removed")
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong!")

        return redirect('cart')
