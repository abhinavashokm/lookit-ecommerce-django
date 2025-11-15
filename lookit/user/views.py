from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "user/login.html")

def signup(request):
    return render(request, "user/signup.html")

def otp_verification(request):
    return render(request, "user/otp_verification.html")