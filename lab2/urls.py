from django.urls import path
from lab2 import views

urlpatterns = [
    path("lab2/", views.lab2, name="lab2"),
]
