from django.shortcuts import render
from core.decorators import admin_required

# Create your views here.
@admin_required
def admin_list_coupon(request):
    return render(request, 'coupon/admin/list.html')

@admin_required
def admin_add_coupon(request):
    return render(request, "coupon/admin/add_coupon.html")

@admin_required
def admin_edit_coupon(request):
    return render(request, "coupon/admin/edit_coupon.html")