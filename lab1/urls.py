from django.urls import path
from lab1 import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lab1/", views.lab1, name="lab1"),
]
