from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import razorpay
from .models import Payment
from order.models import Order, OrderItems
from cart.models import Cart
from order.utils import reduce_stock_for_order
import json


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def create_razorpay_order(request):
    
    # --cart is empty validation------------------------------
    cart_count = Cart.objects.filter(user=request.user).count()
    if cart_count == 0:
        return JsonResponse({'cart_empty':True})
    
    data = json.loads(request.body)
    order_id = data.get('order_id')
    order = None
    if order_id:
        order = Order.objects.get(id=order_id)
    

    amount = 20000  # Rs. 200 in paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture='0')
    )
    
    # Save order in database
    Payment.objects.create(
        user = request.user,
        order = order,
        razorpay_order_id=razorpay_order['id'],
        amount=amount,
        status='Created'
    )

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': reverse('razorpay_paymenthandler'),
        'name':'LookIt'
    }
    
    return JsonResponse(context)

@csrf_exempt
@login_required
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Capture payment
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            razorpay_client.payment.capture(payment_id, payment.amount)

            # Update payment record
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()
            
            #fetch related order and update payment status
            order = payment.order
            order.payment_method = Order.PaymentMethod.ONLINE_PAYMENT
            order.items.update(order_status = OrderItems.OrderStatus.PLACED, payment_status = OrderItems.PaymentStatus.PAID, placed_at=timezone.now())
            order.save()
            
            # --handle stock count of the product---
            reduce_stock_for_order(order.id)

            return redirect('order-success', order_uuid=order.uuid)
        
        except razorpay.errors.SignatureVerificationError:
            
            # Update payment as failed
            Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(status='Failed')
            return redirect('order-failed', order_uuid=order.uuid)
        
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return HttpResponseBadRequest("Invalid request method")