from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from TodoAlRojo.models import *
from TodoAlRojo.forms import RegistroFormulario, LoginFormulario


def go_home_page(request):
    return render(request, 'home.html')

def go_homeLogIn_page(request):
    return render(request, 'home-LogIn.html')

def go_carta_page(request):
    return render(request, 'Carta.html')

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

#CARTA Y PEDIDOS
def cargar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Carta.html', {'productos': productos})

@login_required
def carta(request):
    productos = Producto.objects.all()
    carrito = Carrito.objects.filter(cliente=request.user, activo=True).first()
    return render(request, 'CartaPedir.html', {'productos': productos, 'carrito': carrito})

@login_required
def agregar_a_carrito(request, producto_id):
    cliente = request.user
    producto = get_object_or_404(Producto, id=producto_id)

    # Busca o crea un carrito
    carrito, creado = Carrito.objects.get_or_create(cliente=cliente, activo=True)

    # Busca o crea un item dentro del carrito
    item, item_creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not item_creado:
        item.cantidad += 1
        item.save()

    return redirect('carta_pedir')

@login_required
def eliminar_item_carrito(request, item_id):
    item = ItemCarrito.objects.get(id=item_id)
    if item.carrito.cliente == request.user:
        item.delete()
    return redirect('carta_pedir')

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
                    return redirect('home-login')
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
    return redirect('home')

#ERRORES
def error_403(request, exception=None):
    return render(request, '403.html', status=403)

def error_404(request, exception=None):
    return render(request, '404.html', status=404)