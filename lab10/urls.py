from django.urls import path
from lab10 import views

urlpatterns = [
    path("lab10/", views.lab10, name="lab10"),
]
