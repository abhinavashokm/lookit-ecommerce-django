from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from user.models import User


# custom decorator
def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/admin/login/',  # your custom login
    )(view_func)
    return decorated_view_func


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
    return render(request, "staff/dashboard.html")


def admin_logout(request):
    logout(request)
    return redirect("admin-login")


""" ============================================
    USER MANAGEMENT
============================================ """


def admin_user_management(request):
    user_list = User.objects.all()
    return render(request, "staff/user/list.html",{'users': user_list})


def admin_view_user(request, user_id):
    user_data = User.objects.get(id=user_id)
    return render(request, "staff/user/view_user.html", {"user":user_data})

def admin_edit_user(request):
    return render(request, "staff/user/edit.html")

def admin_block_user_toggle(request, user_id):
    user_data = User.objects.get(id=user_id)
    user_data.is_active = not user_data.is_active
    user_data.save()
    return redirect('admin-view-user',user_id = user_id)

def admin_add_staff(request):
    return render(request, "staff/user/add_staff.html")

def admin_view_staff(request, staff_id):
    staff_data = User.objects.get(id=staff_id)
    return render(request, "staff/user/view_staff.html",{"staff":staff_data})
