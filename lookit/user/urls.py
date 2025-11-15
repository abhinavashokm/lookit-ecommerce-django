from django.urls import path
from django.contrib.auth import views as auth_views
from .views import user_login, signup, otp_verification, user_logout, reset_password

urlpatterns = [
    path("", user_login, name="user-login"),
    path("signup/", signup, name="user-signup"),
    path("signup/otp/", otp_verification, name="signup-otp"),
    path("logout/", user_logout, name="user-logout"),
    
    # password reset paths
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(template_name="user/auth/forgot_password.html"),
        name="forgot-password",
    ),
    path(
        'password-reset-sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/auth/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/auth/reset_password_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        'reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/auth/reset_password_complete.html"
        ),
        name="password_reset_complete",
    ),
]
