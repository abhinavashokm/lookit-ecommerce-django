from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import ExpressionWrapper, DecimalField, F, Sum, Count, Value
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from user.models import Address
from .models import Order, OrderItems
from product.models import Product, Style
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.core.paginator import Paginator



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
    
    cart_item_count = order_items.count()
    if not cart_item_count:
        messages.error(request, "PLEASE ADD ITEMS TO CONTINUE")
        return redirect('cart')

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
    
    #---handle error if no address is selected----------------
    if address_id == '0':
        messages.error(request, "PLEASE SELECT AN ADDRESS")
        return redirect('checkout')
    
    try:
        address = Address.objects.get(id=address_id, user=user)
    except Exception as e:
        messages.error(request, e)
        return redirect('checkout')

    # ---products in order------------------------------------------------
    cart_items = (
        Cart.objects.filter(user=request.user)
        .select_related('variant')
        .annotate(
            sub_total=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            delivery_fee=Value(
                0, output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            discount=Value(
                0, output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            tax=ExpressionWrapper(
                (F('variant__product__price') * F('quantity')) * Decimal('0.05'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )
        .annotate(
            total_amount=ExpressionWrapper(
                F('sub_total')
                + F('tax')
                + F('delivery_fee')
                - F('discount'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )

    # ---total price of all items in cart considering quantity---------
    order_summary = cart_items.aggregate(
        total_sub_total=Sum('sub_total'),
        total_delivery_fee=Sum('delivery_fee'),
        total_tax=Sum('tax'),
        total_discount=Sum('discount'),
        grand_total_amount=Sum('total_amount'),
    )
    total_items = cart_items.count()


    order = None
    try:
        with transaction.atomic():
            
            order = Order.objects.create(
                user=user,
                address=address,
                total_items = total_items,
                sub_total=order_summary.get('total_sub_total'),
                delivery_total=order_summary.get('total_delivery_fee'),
                discount_total=order_summary.get('total_discount'),
                tax_total=order_summary.get('total_tax'),
                grand_total=order_summary.get('grand_total_amount'),
            )
            for item in cart_items:
                OrderItems.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    unit_price=item.variant.product.price,
                    sub_total=item.sub_total,
                    delivery_fee = item.delivery_fee,
                    discount_amount = item.discount,
                    tax_amount = item.tax,
                    total = item.total_amount  # final line total
                )

    except Exception as e:
        messages.error(request, e)
        print(e)
        return redirect('checkout')

    return redirect('payment-page', order_id=order.id)


@login_required
def payment_page(request, order_id):
    order = Order.objects.get(id=order_id)
    address = order.address
    return render(request, "order/payment.html/", {"order": order, "address": address})


@login_required
def place_order(request, order_id):
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')

        # ---check if payment method is valid
        if payment_method not in Order.PaymentMethod.values:
            messages.error("Invalid Payment Method")
            return redirect('payment-page', order_id=order_id)

        try:
            with transaction.atomic():
                Order.objects.filter(id=order_id).update(
                    payment_method=Order.PaymentMethod.COD
                )
                OrderItems.objects.filter(order_id=order_id).update(
                    order_status=OrderItems.OrderStatus.PLACED,
                    payment_status=Order.PaymentMethod.COD,
                )
                messages.success(request, "ORDER PLACED SUCCESSFULLY")
        except Exception as e:
            messages.error(request, e)
            return redirect('payment-page', order_id=order_id)

        # ---empty the cart of user--------------------
        Cart.objects.filter(user=request.user).delete()
        # ---redirect to order success page---------------
        return redirect('order-success', order_id=order_id)


@login_required
def order_success_page(request, order_id):
    order = (
        Order.objects.get(id=order_id)
    )
    order_items = OrderItems.objects.filter(order_id=order_id)
    address = order.address
    return render(
        request,
        "order/order_success.html",
        {'order': order, "address": address, "order_items": order_items},
    )


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related('items')
        .order_by('-created_at')
    )
    return render(request, "order/my_orders.html", {"orders": orders})

@login_required
def track_order(request, order_item_id):
    order_item = OrderItems.objects.get(id=order_item_id)
    delivery_address = order_item.order.address
    return render(request, "order/track_order.html",{"order":order_item, "address":delivery_address})



"""
---------ADMIN SIDE------------------------------------------------------------------------- 
"""

def admin_list_orders(request):
    order_items = OrderItems.objects.all().order_by('-created_at')
    
    search = request.GET.get('search')
    if search:
        order_items = order_items.filter(Q(order__user__full_name__icontains = search) | Q(variant__product__name__icontains = search))

    # pagination
    paginator = Paginator(order_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "order/admin/list.html",{"page_obj": page_obj})

def admin_order_details(request):
    return render(request, "order/admin/order_details.html")