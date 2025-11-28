from django.urls import path
from .views import (
    checkout,
    payment_page,
    create_order,
    place_order,
    order_success_page,
    my_orders,
    track_order,
    admin_list_orders,
    admin_order_details,
    admin_update_delivery_status,
)

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("create-order/", create_order, name="create_order"),
    path("payment/<order_id>/", payment_page, name="payment-page"),
    path("place-order/<order_id>/", place_order, name="place-order"),
    path("order-success/<order_id>/", order_success_page, name="order-success"),
    path("my-orders/", my_orders, name="my-orders"),
    path("track-order/<order_item_id>/", track_order, name="track-order"),
    path("admin/list-orders/", admin_list_orders, name="admin-list-orders"),
    path("admin/order-details/<order_item_id>/", admin_order_details, name="admin-order-details"),
    path("admin/update-delivery-status/<order_item_id>/", admin_update_delivery_status, name="update-delivery-status"),
]
