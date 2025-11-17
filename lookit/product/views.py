from django.shortcuts import render

# Create your views here.
def admin_list_products(request):
    return render(request,"product/admin/list.html")

def admin_add_product(request):
    return render(request, "product/admin/add_product.html")

def admin_add_variant(request):
    return render(request, "product/admin/add_variant.html")

def admin_list_variants(request):
    return render(request, "product/admin/list_variants.html")

