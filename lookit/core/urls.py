from django.urls import path
from .views import home, explore

urlpatterns = [
    path("",home, name="index"),
    path("explore/", explore, name="explore")
]