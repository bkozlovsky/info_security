from django.urls import path
from lab9 import views

urlpatterns = [
    path("lab9/", views.lab9, name="lab9"),
]
