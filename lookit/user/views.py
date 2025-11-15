from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            # create session
            login(request, user)
            return redirect('index')
        print("not authenticated")
        # message = "Invalid Credentials"
        print(request.POST)

    return render(request, "user/login.html")


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        referral_code = request.POST.get('referral_code')
        password = request.POST.get('password')
        new_user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            referral_code=referral_code,
        )
        new_user.save()
        return redirect('index')

    return render(request, "user/signup.html")


def otp_verification(request):
    return render(request, "user/otp_verification.html")


def user_logout(request):
    logout(request)
    return redirect('user-login')
