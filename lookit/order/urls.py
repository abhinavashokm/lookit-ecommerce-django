from django.urls import path
from .views import checkout, payment_page, create_order, place_order, order_success_page, my_orders

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("create-order/", create_order, name="create_order"),
    path("payment/<order_id>/", payment_page, name="payment-page"),
    path("place-order/<order_id>/", place_order, name="place-order"),
    path("order-success/<order_id>/", order_success_page, name="order-success"),
    path("my-orders/", my_orders, name="my-orders")
]
