from random import randint
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import OuterRef, Exists
from . import models


def generate_otp():
    return f"{randint(0, 999999):06d}"


def send_otp_email(email, otp):
    subject = "Your LookIt Signup OTP"
    message = (
        f"Your OTP for LookIt signup is: {otp}\n\nDo not share this code with anyone."
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print("sent otp ", otp)
    send_mail(subject, message, from_email, recipient_list)


def generate_referral_code():
    return uuid.uuid4().hex[:10].upper()

def send_email_verification(user, new_email, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verify_url = request.build_absolute_uri(
        f"/user/verify-email/{uid}/{token}/?new_email={new_email}"
    )

    # Send email
    send_mail(
        subject="Verify your new email",
        message=f"Click this link to verify: {verify_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[new_email],
    )
    

def remove_wishlist_item(user, product_id):
    exist = models.Wishlist.objects.filter(user=user, product_id=product_id).exists()
    if exist:
        models.Wishlist.objects.get(user=user, product_id=product_id).delete()
        
def annotate_wishlist_products(user, products_set):
    """add in_wishlist = True if product is on users wishlist"""
    wishlist_exist_sq = models.Wishlist.objects.filter(user=user, product_id=OuterRef('id'))
    annotated_product_set = products_set.annotate(in_wishlist=Exists(wishlist_exist_sq))
    return annotated_product_set
    