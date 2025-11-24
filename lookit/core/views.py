from django.shortcuts import render, redirect
from product.models import Product


def home(request):
    user = request.user
    new_arrivals = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('-created_at')[:8]
    featured = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('created_at')[:4]
    return render(request, "core/index.html",{'user':user, 'new_arrivals': new_arrivals, 'featured':featured})


        