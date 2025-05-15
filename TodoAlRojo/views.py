from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from TodoAlRojo.models import *

from TodoAlRojo.forms import RegistroFormulario, LoginFormulario


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

def go_GestionCocinero_page(request):
    return render(request, 'GestionCocinero.html')

def go_GestionCamarero_page(request):
    return render(request, 'GestionCamarero.html')

def go_GestionAdministrador_page(request):
    return render(request, 'GestionAdmin.html')

#FUNCIONES
def cargarTablaMesas(request):
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'Mesas.html', {'mesas': mesas})


def cambiar_estado(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.estado = 'DISPONIBLE' if mesa.estado == 'OCUPADA' else 'OCUPADA'
    mesa.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'nuevo_estado': mesa.estado,
            'texto_estado': mesa.get_estado_display(),
            'mesa_id': mesa_id
        })
    return redirect('mesas')

#AUTENTIFICACIÓN
def es_admin (usuario):
    if not usuario.is_authenticated or not usuario.rol == 'admin':
        raise PermissionDenied
    return True

def es_camarero (usuario):
    if not usuario.is_authenticated or not usuario.rol == 'camarero' or not usuario.role == 'admin':
        raise PermissionDenied
    return True

def es_cocinero (usuario):
    if not usuario.is_authenticated or not usuario.rol == 'cocinero' or not usuario.role == 'admin':
        raise PermissionDenied
    return True

#REGISTRO Y LOGIN
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

#ERRORES
def error_403(request, exception=None):
    return render(request, '403.html', status=403)

def error_404(request, exception=None):
    return render(request, '404.html', status=404)