from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def lab1(request):
    return render(request, "lab1.html")
