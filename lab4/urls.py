from django.urls import path
from lab4 import views

urlpatterns = [
    path("lab4/", views.lab4, name="lab4"),
]
