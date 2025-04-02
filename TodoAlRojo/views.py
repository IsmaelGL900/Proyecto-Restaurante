from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def go_home_page(request):
    return render(request, 'home.html')

def go_mesas_page(request):
    return render(request, 'mesas.html')