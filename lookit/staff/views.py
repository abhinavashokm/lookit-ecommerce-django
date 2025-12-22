from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from user.models import User
from django.db.models import Q
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from core.decorators import admin_required
from .utils import (
    get_top_selling_products,
    get_top_selling_styles,
    get_top_selling_brands,
    get_sales_performance,
)


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = authenticate(email=email, password=password)

        if admin:
            if admin.is_staff:
                login(request, admin)
                return redirect("admin-dashboard")
            messages.error(request, "You do not have admin access.")
        else:
            messages.error(request, "Invalid Credentials")

    # redirect authenticated users
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('index')
        return redirect('admin-dashboard')

    return render(request, 'staff/login.html')


@admin_required
def admin_dashboard(request):
    top_selling_products = get_top_selling_products()
    top_selling_styles = get_top_selling_styles()
    top_selling_brands = get_top_selling_brands()
    sales_performance_values = get_sales_performance()
    return render(
        request,
        "staff/dashboard.html",
        {
            "top_selling_products": top_selling_products,
            "top_selling_styles": top_selling_styles,
            "top_selling_brands": top_selling_brands,
            "sales_performance_values":sales_performance_values,
        },
    )


def admin_logout(request):
    logout(request)
    return redirect("admin-login")


""" ============================================
    USER MANAGEMENT
============================================ """


@admin_required
def admin_user_management(request):
    users = User.objects.all()

    search_key = request.GET.get('search', '').strip()
    role = request.GET.get('role', '').strip()
    status = request.GET.get('status', '').strip()
    date_filter = request.GET.get('date', '').strip()

    users = User.objects.all()

    if role:
        is_staff = True if role == 'staff' else False
        users = users.filter(is_staff=is_staff)

    if status:
        is_active = True if status == 'active' else False
        users = users.filter(is_active=is_active)

    # ---- DATE filter ----
    if date_filter:
        today = date.today()

        if date_filter == 'today':
            users = users.filter(created_at__date=today)

        elif date_filter == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            users = users.filter(created_at__date__gte=start_of_week)

        elif date_filter == 'month':
            users = users.filter(
                created_at__year=today.year, created_at__month=today.month
            )
        elif date_filter == 'year':
            users = users.filter(created_at__year=today.year)

    if search_key:
        users = users.filter(
            Q(full_name__icontains=search_key) | Q(email__icontains=search_key)
        )

    # pagination
    paginator = Paginator(users, 6)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, "staff/user/list.html", {'page_obj': page_obj})


@admin_required
def admin_view_user(request, user_id):
    user_data = User.objects.get(id=user_id)
    return render(request, "staff/user/view_user.html", {"user": user_data})


@admin_required
def admin_edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "staff/user/edit.html", {"user": user})


@admin_required
def admin_block_user_toggle(request, user_id):
    user_data = User.objects.get(id=user_id)
    user_data.is_active = not user_data.is_active
    user_data.save()
    if user_data.is_active:
        messages.success(request, f"UNBLOCKED USER")
    else:
        messages.success(request, f"BLOCKED USER")

    return redirect('admin-view-user', user_id=user_id)


@admin_required
def admin_add_staff(request):
    return render(request, "staff/user/add_staff.html")


@admin_required
def admin_view_staff(request, staff_id):
    staff_data = User.objects.get(id=staff_id)
    return render(request, "staff/user/view_staff.html", {"staff": staff_data})
