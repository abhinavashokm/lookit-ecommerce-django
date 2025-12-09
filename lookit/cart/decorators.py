from .models import Cart
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def cart_not_empty_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cart_count = Cart.objects.filter(user=request.user).count()
        if cart_count == 0:
            messages.error(request, "Cart is empty — please add items to continue")
            return redirect('cart')
        return view_func(request, *args, **kwargs)
    return wrapper
