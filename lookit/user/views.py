from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, OTP
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .utils import generate_otp, generate_referral_code, send_otp_email
from datetime import timedelta
from django.utils import timezone


# custom decorator
def user_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and not u.is_staff, login_url='/login/'
    )(view_func)
    return decorated_view_func


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if not user.is_staff:
                # create session
                login(request, user)
                return redirect('index')
            messages.error(
                request, "Admin accounts cannot sign in from the user login page."
            )
        else:
            messages.error(request, "Invalid email or password")

    # redirect authenticated users
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin-dashboard')
        return redirect('index')

    return render(request, "user/login.html")


def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name').strip()
        referral_code = request.POST.get('referral_code').strip()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(
                request,
                "user/signup.html",
                {
                    'full_name': full_name,
                    'email': email,
                    'referral_code': referral_code,
                },
            )

        request.session['signup_data'] = {
            'full_name': full_name,
            'email': email,
            'referral_code': referral_code,
            'password': password,
        }

        otp = generate_otp()
        send_otp_email(email, otp)
        OTP.objects.create(email=email, code = otp) 

        return redirect('signup-otp')

    # redirect authenticated users
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin-dashboard')
        return redirect('index')
    
    expiry_time = timezone.now() + timedelta(minutes=2)
    # Store expiry in session so it survives page reload
    request.session["otp_expires_at"] = expiry_time.timestamp()

    return render(request, "user/signup.html", {"otp_expires_at": expiry_time.timestamp()})


def otp_verification(request):
    if request.method == "POST":
        email = request.session['signup_data'].get('email')
        otp_entered = request.POST.get('otp')
        otp_record = OTP.objects.filter(email=email, code=otp_entered).last()
        raw_password = request.session['signup_data'].get('password')
        
        if otp_record and otp_record.is_valid():
            print(request.session['signup_data'].get('email'))
            new_user = User.objects.create_user(
                email=request.session['signup_data'].get('email'),
                password=raw_password,
                full_name=request.session['signup_data'].get('full_name'),
                referred_by=request.session['signup_data'].get('referral_code'),
                referral_code=generate_referral_code(),
            )
            new_user.save()
            auth_user = authenticate(
                request, email=new_user.email, password=raw_password
            )
            login(request, auth_user)
            return redirect('index')
        else:
            messages.error(request, "Incorrect OTP. Please try again.")

    return render(request, "user/otp_verification.html")


def user_logout(request):
    logout(request)
    return redirect('user-login')
