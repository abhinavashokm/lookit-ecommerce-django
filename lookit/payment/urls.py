from django.urls import path
from payment import views

urlpatterns = [
    path('', views.homepage, name='online-payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]