from django.urls import path
from payment import views

urlpatterns = [
    path('paymenthandler/', views.paymenthandler, name='razorpay_paymenthandler'),
    path("create_razorpay_order/", views.create_razorpay_order, name="create_razorpay_order"),
]