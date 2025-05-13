from django.urls import path
from lab5 import views

urlpatterns = [
    path("lab5/", views.lab5, name="lab5"),
]
