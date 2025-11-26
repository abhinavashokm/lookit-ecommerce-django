from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, OTP, Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import generate_otp, generate_referral_code, send_otp_email
from datetime import timedelta
from django.utils import timezone
from cloudinary.uploader import upload


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            # create session
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password")

    # redirect authenticated users
    if request.user.is_authenticated:
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

        return redirect('signup-send-otp')

    # redirect authenticated users
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, "user/signup.html")


def send_otp(request):
    email = request.session['signup_data'].get('email')
    otp = generate_otp()
    send_otp_email(email, otp)
    OTP.objects.create(email=email, code=otp)

    expiry_time = timezone.now() + timedelta(minutes=1)
    # Store expiry in session so it survives page reload
    request.session["otp_expires_at"] = expiry_time.timestamp()
    return redirect('signup-otp')


def otp_verification(request):
    if request.method == "POST":
        email = request.session['signup_data'].get('email')
        otp_entered = request.POST.get('otp')
        otp_record = OTP.objects.filter(email=email, code=otp_entered).last()
        raw_password = request.session['signup_data'].get('password')

        if otp_record and otp_record.is_valid():
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
            messages.success(request, "ACCOUNT CREATED SUCCESSFULLY")
            return redirect('index')
        else:
            messages.error(request, "Incorrect OTP. Please try again.")

    # redirect authenticated users
    if request.user.is_authenticated:
        return redirect('index')

    expiry_time = request.session["otp_expires_at"]
    return render(
        request, "user/otp_verification.html", {"otp_expires_at": expiry_time}
    )


def user_logout(request):
    logout(request)
    return redirect('user-login')


"""
---USER PROFILE-----------
"""


@login_required
def account_details(request):
    user = request.user
    return render(request, 'user/profile/account_details.html', {"user": user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        try:

            full_name = request.POST.get('full_name').strip()
            email = request.POST.get('email').strip().lower()
            phone = request.POST.get('phone').strip()
            gender = request.POST.get('gender')
            profile_pic = request.FILES.get('profile_image')

            dob = request.POST.get('dob')
            if dob == "":
                dob = None  # empty string in date field will raise error

            # ---upload profile pic if it exist--------------------------
            img_url = None
            image_public_id = None
            if profile_pic:
                print("undu")
                # ---upadate existing profile pic---------------------------
                if request.user.profile_img_url:
                    result = upload(
                        profile_pic,
                        folder=f"profile_images/{request.user.id}",
                        public_id=request.user.profile_img_public_id,
                        overwrite=True,
                        invalidate=True,
                        transformation=[
                            {
                                'width': 500,
                                'height': 500,
                                'crop': 'fill',  # crop to fill box, no empty space
                                'gravity': 'face',  # smart focus on detected face
                            },
                            {
                                'quality': 'auto',  # auto-tune quality
                                'fetch_format': 'auto',  # serve as webp/avif/jpg depending on browser
                            },
                        ],
                    )
                    img_url = result['secure_url']
                    image_public_id = request.user.profile_img_public_id

                # ---add profile pic for the first time---------------------
                else:
                    result = upload(
                        profile_pic,
                        folder=f"profile_images/{request.user.id}",
                        transformation=[
                            {
                                'width': 500,
                                'height': 500,
                                'crop': 'fill',
                                'gravity': 'face',
                            },
                            {
                                'quality': 'auto',
                                'fetch_format': 'auto',
                            },
                        ],
                    )
                    img_url = result['secure_url']
                    image_public_id = result['public_id']

            else:
                img_url = request.user.profile_img_url
                image_public_id = request.user.profile_img_public_id

            # ---if email is same just update the rest of the details------
            if email == request.user.email:
                user = User.objects.filter(email=request.user.email).update(
                    full_name=full_name,
                    phone=phone,
                    dob=dob,
                    gender=gender,
                    profile_img_url=img_url,
                    profile_img_public_id=image_public_id,
                )
                messages.success(request, "PROFILE UPDATED")
                return redirect('account-details')

            # ---check email already exist----------------------------------
            email_already_exist = User.objects.filter(email=email).exists()
            if email_already_exist:
                messages.error(request, "AN ACCOUNT WITH THIS EMAIL ALREADY EXIST")
                return redirect('edit-profile')

            # ---update details including email-------------------------
            user = User.objects.filter(email=request.user.email).update(
                email=email,
                full_name=full_name,
                phone=phone,
                dob=dob,
                gender=gender,
                profile_img_url=img_url,
                profile_img_public_id=image_public_id,
            )
            messages.success(request, "PROFILE UPDATED")
            return redirect('account-details')
        # ---catch any exceptions
        except Exception as e:
            messages.error(request, e)
            return redirect('edit-profile')

    user = request.user
    return render(request, "user/profile/edit_profile.html", {"user": user})


@login_required
def add_address(request):
    if request.method == "POST":
        user = request.user
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        type = request.POST.get('type')

        # ---optional_fields-----------------------
        is_default = request.POST.get('is_default')
        if not is_default:
            is_default = False
        second_phone = request.POST.get('second_phone')

        print(request.POST)
        try:
            Address.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                second_phone=second_phone,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode,
                type=type,
                is_default=is_default,
            )
            messages.success(request, "NEW ADDRESS ADDED")
        except Exception as e:
            print(e)
            messages.error(request, e)

    return redirect('checkout')

@login_required
def edit_address(request):
    if request.method == "POST":
        user = request.user
        address_id = request.POST.get('address_id')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        type = request.POST.get('type')

        # ---optional_fields-----------------------
        is_default = request.POST.get('is_default')
        if not is_default:
            is_default = False
        second_phone = request.POST.get('second_phone')
        
        print(request.POST)
        try:
            Address.objects.filter(id=address_id).update(
                user=user,
                full_name=full_name,
                phone=phone,
                second_phone=second_phone,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode,
                type=type,
                is_default=is_default,
            )
            #---if it is default address set all other address is_default = false---------------
            if is_default:
                Address.objects.filter(user=user).exclude(id=address_id).update(is_default=False)
                
            messages.success(request, "ADDRESS UPDATED")
        except Exception as e:
            print(e)
            messages.error(request, e)

    return redirect('checkout')

@login_required
def delete_address(request):
    if request.method == "POST":
        address_id = request.POST.get('address_id')
        try:
            Address.objects.filter(id=address_id).update(is_active=False)
            messages.success(request, "ADDRESS DELETED")
        except Exception as e:
            messages.error(request, e)

    return redirect('checkout')
