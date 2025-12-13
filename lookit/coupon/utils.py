from .models import Coupon


def is_valid_coupon(code):
    coupon = Coupon.objects.filter(code=code).first()
    if coupon and coupon.status == 'ACTIVE':
        return True
    return False
