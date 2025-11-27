from django.urls import path
from .views import checkout, payment_page

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("payment", payment_page, name="payment-page"),
]