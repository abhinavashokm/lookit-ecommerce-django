from random import randint
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(randint(000000, 999999))


def send_otp_email(email, otp):
    subject = "Your LookIt Signup OTP"
    message = (
        f"Your OTP for LookIt signup is: {otp}\n\nDo not share this code with anyone."
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print("sent otp ", otp)
    send_mail(subject, message, from_email, recipient_list)


def get_referral_code():
    return str(randint(000000, 999999))
