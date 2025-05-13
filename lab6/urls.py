from django.urls import path
from lab6 import views

urlpatterns = [
    path("lab6/", views.lab6, name="lab6"),
]
