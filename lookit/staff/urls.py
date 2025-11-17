from django.urls import path
from .views import admin_login, admin_dashboard, admin_logout, admin_user_management


urlpatterns = [
    path("login/",admin_login, name="admin-login"),
    path("", admin_dashboard, name="admin-dashboard"),
    path("logout/", admin_logout, name="admin-logout"),
    path("user_management/", admin_user_management, name="admin-user")
]