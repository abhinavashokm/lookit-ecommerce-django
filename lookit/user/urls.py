from django.urls import path
from .views import login, signup, otp_verification
urlpatterns = [
    path("",login, name="user-login"),
    path("signup/",signup, name="user-signup"),
    path("signup/otp/", otp_verification, name="signup-otp")
]