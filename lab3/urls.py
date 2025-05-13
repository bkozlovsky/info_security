from django.urls import path
from lab3 import views

urlpatterns = [
    path("lab3/", views.lab3, name="lab3"),
]
