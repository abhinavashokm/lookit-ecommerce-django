from django.urls import path
from .views import checkout, payment_page, create_order

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("create-order/", create_order, name="create_order"),
    path("payment/<order_id>/", payment_page, name="payment-page"),
]
