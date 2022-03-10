
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("welcome to grabit")

def home(request):
    return render(request, "grabit/index.html")

def ads(request):
    return render(request, "grabit/ads.html")