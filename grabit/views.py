
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("welcome to grabit")

def home(request):
    return render(request, "grabit/index.html")

def register(request):
    return render(request, "grabit/register.html")

def logIn(request):
    return render(request, "grabit/login.html")