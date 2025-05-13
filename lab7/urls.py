from django.urls import path
from lab7 import views

urlpatterns = [
    path("lab7/", views.lab7, name="lab7"),
]
