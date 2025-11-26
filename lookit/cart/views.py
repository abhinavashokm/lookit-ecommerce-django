from django.shortcuts import render
from .models import Cart
from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user = request.user)
    
    return render(request,'cart/cart.html', {"cart_items":cart_items})
