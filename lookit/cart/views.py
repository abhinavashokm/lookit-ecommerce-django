from django.shortcuts import render
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from decimal import Decimal, ROUND_HALF_UP

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).select_related('variant')
    
    #cart price summary
    sub_total = cart_items.aggregate(sub_total = Sum(F('variant__product__price') * F('quantity')))['sub_total'] or 0
    tax = sub_total * Decimal(0.05)
    #ROUND_HALF_UP -> ROUNDING METHOD USED - less than 0.5 then reduce, greater than or equal to 0.5 then increase(BANKERS STYLE)
    tax = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
 
    cart_summary = {
        "sub_total": sub_total,
        "tax" : tax,
        "grand_total": sub_total + tax
    }
    
    return render(request,'cart/cart.html', {"cart_items":cart_items, "cart_summary": cart_summary})
