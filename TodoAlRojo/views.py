from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def go_home_page(request):
    return render(request, 'home.html')

def go_mesas_page(request):
    return render(request, 'mesas.html')

def go_login_page(request):
    return render(request, 'Login.html')

def go_registrarse_page(request):
    return render(request, 'Registrarse.html')

def go_gestion_page(request):
    return render(request, 'Gestion.html')