
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "grabit/index.html")

def register(request):
    return render(request, "grabit/register.html")

def logIn(request):
    return render(request, "grabit/login.html")

def edit_profile(request):
    return render(request, "grabit/edit_profile.html")

def view_profile(request):
    return render(request, "grabit/view_profile.html")