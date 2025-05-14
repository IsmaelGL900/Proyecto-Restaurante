from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse

from TodoAlRojo.forms import RegistroFormulario, LoginFormulario
from TodoAlRojo.models import Usuario


def go_home_page(request):
    return render(request, 'home.html')

def go_mesas_page(request):
    return render(request, 'Mesas.html')

def go_login_page(request):
    return render(request, 'Login.html')

def go_registrarse_page(request):
    return render(request, 'Registrarse.html')

def go_gestion_page(request):
    return render(request, 'Gestion.html')

def go_GestionCocinero_page(request):
    return render(request, 'GestionCocinero.html')

def go_GestionCamarero_page(request):
    return render(request, 'GestionCamarero.html')

def go_GestionAdministrador_page(request):
    return render(request, 'GestionAdmin.html')

def registrar_usuario(request):
    form = RegistroFormulario()
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save(commit=False)
            usuario_nuevo.set_password(form.cleaned_data['password'])
            usuario_nuevo.save()
            return redirect( 'login' )
    else:
        return render(request,"Registrarse2.html", {'form':form})

def loguearse(request):
    form = LoginFormulario()
    if request.method == 'POST':
        form = LoginFormulario(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)

                rol = usuario.rol

                if rol == 'cliente':
                    return redirect('home')
                elif rol == 'admin':
                    return redirect('GestionAdmin')
                elif rol == 'camarero':
                    return redirect('GestionCamarero')
                elif rol == 'cocinero':
                    return redirect('GestionCocinero')
    else:
        return render(request, "Login2.html", {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login')