from django.shortcuts import render, redirect
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
import json
from django.http import JsonResponse

@login_required
def cart(request):
    cart_items = (
        Cart.objects.filter(user=request.user)
        .select_related('variant')
        .annotate(
            sub_total_per_product=ExpressionWrapper(
                F('variant__product__price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
    )
    # cart price summary
    sub_total = (
        cart_items.aggregate(
            sub_total=Sum(F('variant__product__price') * F('quantity'))
        )['sub_total']
        or 0
    )
    tax = sub_total * Decimal(0.05)
    # ROUND_HALF_UP -> ROUNDING METHOD USED - less than 0.5 then reduce, greater than or equal to 0.5 then increase(BANKERS STYLE)
    tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    cart_summary = {"sub_total": sub_total, "tax": tax, "grand_total": sub_total + tax}
    print(cart_items[0])
    return render(
        request,
        'cart/cart.html',
        {"cart_items": cart_items, "cart_summary": cart_summary},
    )

@login_required
def remove_cart_item(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        try:
            Cart.objects.get(variant_id = variant_id).delete()
            messages.success(request, "ITEM REMOVED FROM CART")
        except Exception as e:
            messages.error(request, e) 
            
    return redirect('cart')

@login_required
def update_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        cart_id = data.get('cart_id')
        variant_id = data.get('variant_id')
        new_quantity = data.get('new_quantity')
        
        try:
            cart_item = Cart.objects.get(id=cart_id, variant_id = variant_id)
            cart_item.quantity = new_quantity
            cart_item.save()
        except Exception as e:
            print("ERROR: ",e)
            
    return JsonResponse(
        {"status": "success", "message": "Quantity updated", "new_quantity": new_quantity}
    )