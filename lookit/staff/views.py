from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


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

def admin_user_management(request):
    return render(request, "staff/user/list.html")


def admin_logout(request):
    logout(request)
    return redirect("admin-login")
