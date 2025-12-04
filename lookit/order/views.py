from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import ExpressionWrapper, DecimalField, F, Sum, Value, When, Case, Min, IntegerField
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from user.models import Address
from .models import Order, OrderItems, ReturnRequest
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date, timedelta
from cloudinary.uploader import upload

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

    # ---handle error if no address is selected----------------
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
                F('sub_total') + F('tax') + F('delivery_fee') - F('discount'),
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
                total_items=total_items,
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
                    delivery_fee=item.delivery_fee,
                    discount_amount=item.discount,
                    tax_amount=item.tax,
                    total=item.total_amount,  # final line total
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
                    placed_at=timezone.now(),
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
    order = Order.objects.get(id=order_id)
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
        .annotate(
        status_priority=Min(
            Case(
                When(items__order_status='OUT_FOR_DELIVERY', then=Value(1)),
                When(items__order_status='SHIPPED', then=Value(2)),
                When(items__order_status='PLACED', then=Value(3)),
                When(items__order_status='DELIVERED', then=Value(4)),
                When(items__order_status='RETURNED', then=Value(5)),
                When(items__order_status='CANCELLED', then=Value(6)),
                default=Value(7),
                output_field=IntegerField(),
            )
        )
    )
        .order_by('status_priority' ,'-created_at')
    )
    #--search functionality----------
    search = request.GET.get('search')
    if search:
        orders = orders.filter(items__variant__product__name__icontains = search)
        
    return render(request, "order/my_orders.html", {"orders": orders})


@login_required
def track_order(request, order_uuid):
    order_item = OrderItems.objects.get(uuid=order_uuid)
    delivery_address = order_item.order.address
    return render(
        request,
        "order/track_order.html",
        {"order": order_item, "address": delivery_address},
    )


@login_required
def cancel_order(request, order_item_uuid):
    try:
        order_item = OrderItems.objects.get(uuid=order_item_uuid)
        if order_item.order.user == request.user:
            order_item.order_status = 'CANCELLED'
            order_item.cancelled_at = timezone.now()
            order_item.save()
            messages.success(request, "Order Cancelled.")
        else:
            messages.error(request, "Unauthorized Access")
    except Exception as e:
        messages.error(request, e)
    return redirect('track-order', order_uuid=order_item_uuid)


@login_required
def return_request_form(request, order_uuid):
    if request.method == "POST":
        print(request.POST)

        order_item = OrderItems.objects.get(uuid=order_uuid)

        reason = request.POST.get('reason')
        comments = request.POST.get('comments')
        
        images = request.FILES.getlist('product_images')
        print(request.FILES)
        print("images",images)

        #---fetch pick up address--------------------------------
        pickup_address_id = request.POST.get('pickup_address_id')
        pickup_address = None
        if pickup_address_id:
            pickup_address = Address.objects.get(id=pickup_address_id)
        else:
            messages.error(request, "Please Select A Pick Up Address")
            
        try:
            with transaction.atomic():
                return_request = ReturnRequest.objects.create(
                    order_item=order_item,
                    reason=reason,
                    comments=comments,
                    pickup_address=pickup_address,
                    amount_paid=order_item.total
                )
                # Assign images to available fields (up to 3)
                if len(images) > 0:
                    result = upload(
                            images[0],
                            folder=f"return_product_images/{request.user.id}",
                            transformation=[
                                {
                                    'width': 500,
                                    'height': 500,
                                    'crop': 'fill',
                                    'gravity': 'face',
                                },
                                {
                                    'quality': 'auto',
                                    'fetch_format': 'auto',
                                },
                            ],
                        )
                    return_request.product_image1 = result['secure_url']
                if len(images) > 1:
                    result = upload(
                            images[1],
                            folder=f"return_product_images/{request.user.id}",
                            transformation=[
                                {
                                    'width': 500,
                                    'height': 500,
                                    'crop': 'fill',
                                    'gravity': 'face',
                                },
                                {
                                    'quality': 'auto',
                                    'fetch_format': 'auto',
                                },
                            ],
                        )
                    return_request.product_image2 = result['secure_url']
                if len(images) > 2:
                    result = upload(
                            images[2],
                            folder=f"return_product_images/{request.user.id}",
                            transformation=[
                                {
                                    'width': 500,
                                    'height': 500,
                                    'crop': 'fill',
                                    'gravity': 'face',
                                },
                                {
                                    'quality': 'auto',
                                    'fetch_format': 'auto',
                                },
                            ],
                        )
                    return_request.product_image3 = result['secure_url']
                return_request.save()
                
                messages.success(request, "Return Request Submitted Successfully")
            
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect('return-request-form', order_uuid=order_uuid)

        return redirect('track_return_request', order_uuid=order_uuid)

    order = OrderItems.objects.get(uuid=order_uuid)
    address_list = Address.objects.filter(user=request.user, is_active=True).order_by(
        '-is_default', '-created_at'
    )
    return render(
        request,
        "order/return_request_form.html",
        {"order": order, "address_list": address_list},
    )

@login_required
def track_return_request(request, order_uuid):
    order_item = OrderItems.objects.get(uuid=order_uuid)
    return_request = order_item.return_request
    
    delivery_address = order_item.order.address
    return render(
        request,
        "order/track_return.html",
        {"order": order_item, "address": delivery_address, "return_request": return_request},
    )


"""
---------ADMIN SIDE------------------------------------------------------------------------- 
"""


def admin_list_orders(request):
    order_items = OrderItems.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    payment_method = request.GET.get('payment_method')
    payment_status = request.GET.get('payment_status')
    order_status = request.GET.get('order_status')
    date_range = request.GET.get('date_range')

    if search:
        order_items = order_items.filter(
            Q(order__user__full_name__icontains=search)
            | Q(variant__product__name__icontains=search)
        )

    if payment_method:
        order_items = order_items.filter(order__payment_method=payment_method.upper())

    if payment_status:
        order_items = order_items.filter(payment_status=payment_status.upper())

    if order_status:
        order_items = order_items.filter(order_status=order_status.upper())

        # ---- DATE filter ----
    if date_range:
        today = date.today()

        if date_range == 'today':
            order_items = order_items.filter(placed_at__date=today)

        elif date_range == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            order_items = order_items.filter(placed_at__date__gte=start_of_week)

        elif date_range == 'month':
            order_items = order_items.filter(
                placed_at__year=today.year, placed_at__month=today.month
            )
        elif date_range == 'year':
            order_items = order_items.filter(placed_at__year=today.year)

    # pagination
    paginator = Paginator(order_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "order/admin/list.html", {"page_obj": page_obj})


def admin_order_details(request, order_item_uuid):
    order_item = OrderItems.objects.get(uuid=order_item_uuid)
    customer = order_item.order.user
    address = order_item.order.address
    return render(
        request,
        "order/admin/order_details.html",
        {"order": order_item, "customer": customer, "address": address},
    )


def admin_update_delivery_status(request, order_item_uuid):
    if request.method == "POST":
        order_status = request.POST.get("order_status")
        try:
            order_item = OrderItems.objects.get(uuid=order_item_uuid)
            if order_status.upper() in OrderItems.OrderStatus.values:
                order_item.order_status = order_status.upper()

                if order_status == 'placed':
                    order_item.placed_at = timezone.now()
                    order_item.shipped_at = None
                    order_item.out_for_delivery_at = None
                    order_item.delivered_at = None
                elif order_status == 'shipped':
                    order_item.shipped_at = timezone.now()
                    order_item.out_for_delivery_at = None
                    order_item.delivered_at = None
                elif order_status == 'out_for_delivery':
                    order_item.out_for_delivery_at = timezone.now()
                    order_item.delivered_at = None
                elif order_status == 'delivered':
                    order_item.delivered_at = timezone.now()
                elif order_status == 'cancelled':
                    order_item.cancelled_at = timezone.now()

                order_item.save()
                messages.success(request, "ORDER STATUS UPDATED SUCCESSFULLY")
            else:
                messages.error(request, "INVALID ORDER STATUS")
        except Exception as e:
            messages.error(request, e)

    return redirect('admin-order-details', order_item_uuid=order_item_uuid)


def admin_list_return_requests(request):
    return_request_list = ReturnRequest.objects.all().select_related('order_item').order_by("-request_date")
    return render(request, 'order/admin/return_request_list.html',{"return_request_list":return_request_list})



def admin_return_details(request, return_request_uuid):
    return_request = ReturnRequest.objects.get(uuid=return_request_uuid)
    order_item = return_request.order_item
    customer = order_item.order.user
    address = order_item.order.address

    return render(
        request,
        "order/admin/return_details.html",
        {"return_request": return_request,"order": order_item, "customer": customer, "address": address},
    )
    

def admin_update_return_status(request, return_request_uuid):
    if request.method == "POST":
        return_status = request.POST.get("return_status")

        if return_status in ReturnRequest.ReturnStatus.values:
            return_request = ReturnRequest.objects.get(uuid=return_request_uuid)
            return_request.status = return_status

            # Set relevant timestamp based on new status
            if return_status == ReturnRequest.ReturnStatus.APPROVED:
                return_request.approved_at = timezone.now()
                return_request.rejected_at = None
                return_request.pickup_scheduled_at = None
                return_request.pickedup_at = None
                return_request.refunded_at = None
            elif return_status == ReturnRequest.ReturnStatus.REJECTED:
                return_request.rejected_at = timezone.now()
                return_request.approved_at = None
                return_request.pickup_scheduled_at = None
                return_request.pickedup_at = None
                return_request.refunded_at = None
            elif return_status == ReturnRequest.ReturnStatus.PICKUP_SCHEDULED:
                return_request.pickup_scheduled_at = timezone.now()
                return_request.pickedup_at = None
                return_request.refunded_at = None
            elif return_status == ReturnRequest.ReturnStatus.PICKED_UP:
                return_request.pickedup_at = timezone.now()
                return_request.refunded_at = None
            elif return_status == ReturnRequest.ReturnStatus.REFUNDED:
                return_request.refunded_at = timezone.now()
 

            return_request.save()
            messages.success(request, "Return status updated successfully.")
        else:
            messages.error(request, "Invalid return status.")

    return redirect("admin-return-details", return_request_uuid=return_request_uuid)


