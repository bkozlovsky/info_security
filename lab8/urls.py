from django.urls import path
from lab8 import views

urlpatterns = [
    path("lab8/", views.lab8, name="lab8"),
    path("lab8/hash_check", views.hash_check, name="lab8_hash_check"),
]
