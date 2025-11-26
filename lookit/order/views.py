from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    return render(request, "order/checkout.html")
