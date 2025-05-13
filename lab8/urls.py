from django.urls import path
from lab8 import views

urlpatterns = [
    path("lab8/", views.lab8, name="lab8"),
]
