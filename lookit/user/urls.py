from django.urls import path
from .views import user_login, signup, otp_verification, user_logout
urlpatterns = [
    path("",user_login, name="user-login"),
    path("signup/",signup, name="user-signup"),
    path("signup/otp/", otp_verification, name="signup-otp"),
    path("logout/",user_logout, name="user-logout")
]