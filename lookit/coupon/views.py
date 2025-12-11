from django.shortcuts import render, redirect
from core.decorators import admin_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Coupon


# Create your views here.
@admin_required
def admin_list_coupon(request):
    coupons = Coupon.objects.all()
    
    #--create pagination object-----
    paginator = Paginator(coupons, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'coupon/admin/list.html',{'page_obj':page_obj})


@admin_required
def admin_add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        discount_type = request.POST.get('discount_type', '').strip()
        discount_value = request.POST.get('discount_value', '').strip()
        min_purchase_amount = request.POST.get('min_purchase_amount', '').strip()
        usage_limit = request.POST.get('usage_limit', '').strip()
        status = request.POST.get('status', '').strip()
        is_active = request.POST.get('is_active') in ['true', 'True', '1', 'on']
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()

        # --validation check: ensure all required fields exist--
        required_fields = {
            'code': code,
            'discount_type': discount_type,
            'discount_value': discount_value,
            'min_purchase_amount': min_purchase_amount,
            'usage_limit': usage_limit,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        print(request.POST)
        if missing_fields:
            messages.error(
                request, f"Missing required fields: {', '.join(missing_fields)}"
            )
            return redirect('admin-add-coupon')
        try:
            Coupon.objects.create(
                code=code,
                discount_type=discount_type,
                discount_value=discount_value,
                min_purchase_amount=min_purchase_amount,
                usage_limit=usage_limit,
                status=status,
                is_active=is_active,
                start_date=start_date,
                end_date=end_date,
            )
            messages.success(request, "Coupon Created Successfully")
            return redirect('admin-list-coupons')
        except Exception as e:
            print("Error: ", e)
            messages.error(request, "Something went wrong")
            return redirect('admin-add-coupon')

    return render(request, "coupon/admin/add_coupon.html")


@admin_required
def admin_edit_coupon(request):
    return render(request, "coupon/admin/edit_coupon.html")
