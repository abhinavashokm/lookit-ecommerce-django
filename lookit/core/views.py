from django.shortcuts import render, redirect


def home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return redirect('admin-dashboard')
    return render(request, "core/index.html",{user:user})

def explore(request):
    return render(request, "core/explore.html")
        