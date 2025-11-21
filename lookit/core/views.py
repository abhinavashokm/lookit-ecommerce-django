from django.shortcuts import render, redirect
from product.models import Product, Style


def home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return redirect('admin-dashboard')
    return render(request, "core/index.html",{user:user})

def explore(request):
    products = Product.objects.all()
    styles = Style.objects.all()
    
    #---search----------------------------
    search_key = request.GET.get('search')
    if search_key:
        products = products.filter(name__icontains = search_key)
        
    #---sort----------------------
    sort = request.GET.get('sort')
    if sort:
        if "price" in sort:
            products = products.order_by(sort)
        elif "name" in sort:
            products = products.order_by(sort)
        
    #----filter---------------------
    style = request.GET.get('style')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if style:
        print(style)
        products = products.filter(style__name__icontains = style)
        for i in products:
            print(i.name, i.style.name)
    if(price_min and price_max):
        products = products.filter(price__range=(price_min, price_max))
    
    return render(request, "core/explore.html",{"page_obj": products, "styles":styles})
        