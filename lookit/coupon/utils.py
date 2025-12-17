from .models import Coupon, CouponUsage
from user.models import User
from cart.models import CartAppliedCoupon

def is_valid_coupon(code):
    coupon = Coupon.objects.filter(code=code).first()
    if coupon and coupon.status == 'ACTIVE':
        return True
    return False


def reduce_coupon_usage_limit(code):
    coupon = Coupon.objects.filter(code=code).first()
    # -1 is for unlimited, so do nothing
    if coupon and coupon.usage_limit != -1:
        coupon.usage_remaining -= 1
        coupon.save()


def update_coupon_usage_remaining(code, new_usage_limit):
    """this function is for updaing coupon remaining usage count when updating coupons fixed usage limit."""
    coupon = Coupon.objects.get(code=code)
    new_usage_limit = int(new_usage_limit)
    
    # if usage limit not changed, do nothing
    # -1 is for unlimited, so do nothing
    print(coupon.usage_limit)
    print(new_usage_limit)
    if coupon.usage_limit != new_usage_limit and coupon.usage_limit != -1:
        #we respect how much coupon already used
        used_count = coupon.usage_limit - coupon.usage_remaining
        new_usage_remaining = new_usage_limit - used_count

        #usage reamining can't be negative value, so in those case set it to zero
        if new_usage_remaining > 0:
            coupon.usage_remaining = new_usage_remaining
        else:
            coupon.usage_remaining = 0
        coupon.save()


def create_coupon_usage_record(coupon, user):
    if coupon and user:
        CouponUsage.objects.create(coupon=coupon, user=user)
        
def coupon_eligibility_check(coupon_code, user):
    """function which return true if user never used the coupon else return false"""
    exists = CouponUsage.objects.filter(coupon__code=coupon_code, user=user)
    if exists:
        return False
    return True

def clear_users_saved_coupon(coupon, user):
    """this function will remove the applied coupon from users savecoupons list and applied coupon"""
    #remove applied coupon
    CartAppliedCoupon.objects.filter(coupon=coupon, user=user).delete()
    #remove from saved coupons
    user = User.objects.get(id=user.id)
    user.saved_coupons.remove(coupon)