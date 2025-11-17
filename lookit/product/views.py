from django.shortcuts import render

# Create your views here.
def admin_list(request):
    return render(request,"product/admin/list.html")

