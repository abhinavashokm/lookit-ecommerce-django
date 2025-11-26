from django.urls import path
from .views import cart, remove_cart_item

urlpatterns = [
    path("", cart, name='cart'),
    path("remove-item/", remove_cart_item, name="remove_cart_item"),
]