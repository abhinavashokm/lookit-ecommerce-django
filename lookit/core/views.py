from django.shortcuts import render
from product.models import Product
from offer.utiils import annotate_offers


def home(request):
    user = request.user
    new_arrivals = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('-created_at')[:8]
    new_arrivals = annotate_offers(new_arrivals) #apply offer discounts
    
    featured = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct().order_by('created_at')[:4]
    featured = annotate_offers(featured) #apply offer_discounts
    
    return render(request, "core/index.html",{'user':user, 'new_arrivals': new_arrivals, 'featured':featured})


        