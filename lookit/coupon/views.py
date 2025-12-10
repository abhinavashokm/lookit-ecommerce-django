from django.shortcuts import render

# Create your views here.
def admin_list_coupon(request):
    return render(request, 'coupon/admin/list.html')