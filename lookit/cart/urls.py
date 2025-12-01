from django.urls import path
from .views import cart, remove_cart_item, update_quantity

urlpatterns = [
    path("", cart, name='cart'),
    path("remove-item/", remove_cart_item, name="remove_cart_item"),
    path("update-quantity/", update_quantity, name="update-quantity")
]