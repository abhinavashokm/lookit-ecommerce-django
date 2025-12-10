from django.urls import path
from . import views

urlpatterns = [
    path("admin/list/", views.admin_list_coupon, name="admin-list-coupons"),
]
