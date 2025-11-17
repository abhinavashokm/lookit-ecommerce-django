from django.urls import path
from .views import admin_list

urlpatterns = [
    path("admin-list/", admin_list, name="admin-list"),
]