from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from pyexpat.errors import messages

from TodoAlRojo.models import *
from TodoAlRojo.forms import RegistroFormulario, LoginFormulario, RegistroAdminFormulario, ProductoAdminFormulario, \
    PersonalizarForm
from django.db.models import Sum

#AUTENTIFICACIÓN
def es_admin (usuario):
    if usuario.is_authenticated and usuario.rol == 'admin':
        return True
    else:
        raise PermissionDenied

def es_camarero (usuario):
    if usuario.is_authenticated and (usuario.rol == 'camarero' or usuario.rol == 'admin'):
        return True
    else:
        raise PermissionDenied


def es_cocinero (usuario):
    if usuario.is_authenticated and (usuario.rol == 'cocinero' or usuario.rol == 'admin'):
        return True
    else:
        raise PermissionDenied
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

def carta_SinCuenta(request):
    productos = Producto.objects.all()
    return render(request, 'Carta.html', {'productos': productos})
@login_required
def go_historial_page(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')
    pedidos_terminados = PedidoTerminado.objects.filter(cliente=request.user).order_by('-fecha')
    return render(request, 'Historial.html', {"pedidos": pedidos, "pedidos_terminados": pedidos_terminados})
@user_passes_test(es_cocinero)
def go_GestionCocinero_page(request):
    return render(request, 'GestionCocinero.html')

@user_passes_test(es_camarero)
def go_GestionCamarero_page(request):
    return render(request, 'GestionCamarero.html')

@user_passes_test(es_admin)
def go_GestionAdministrador_page(request):
    return render(request, 'GestionAdmin.html')

@user_passes_test(es_admin)
def go_cuentas_page(request):
    usuarios = Usuario.objects.all()
    return render(request, 'AdministrarCuentas.html',{'usuarios': usuarios})

@user_passes_test(es_admin)
def go_AdminCarta_page(request):
    productos = Producto.objects.all()
    return render(request, 'AdministrarCarta.html', {'productos': productos})

@user_passes_test(es_admin)
def go_AdminMesas_page(request):
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'AdministrarMesas.html', {'mesas': mesas})

def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    pedidos_terminados = PedidoTerminado.objects.all()
    return render(request, 'PedidosAdmin.html', {'pedidos': pedidos, 'pedidos_terminados': pedidos_terminados})

#FUNCIONES
@user_passes_test(es_camarero)
def cargarTablaMesas(request):
    mesas = Mesa.objects.all().order_by('numero').annotate(
        total_pedidos=Sum('pedido__total')
    )
    pedidos = Pedido.objects.all()
    return render(request, 'Mesas.html', {'mesas': mesas, 'pedidos': pedidos})

def mover_a_pedidos_terminados(pedido):
    terminado = PedidoTerminado.objects.create(
        cliente=pedido.cliente if pedido.cliente else None,
        mesa_numero=pedido.mesa,
        camarero=pedido.camarero if pedido.camarero else None,
        cocinero=pedido.cocinero if pedido.cocinero else None,
        fecha=pedido.fecha,
        total=pedido.total
    )

    for item in pedido.items.all():
        ItemPedidoTerminado.objects.create(
            pedido_terminado=terminado,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario
        )

@user_passes_test(es_camarero)
def cobrar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedidos = mesa.pedido_set.all()

    for pedido in pedidos:
        mover_a_pedidos_terminados(pedido)

    pedidos.delete()

    mesa.estado = 'DISPONIBLE'
    mesa.save()

    return redirect('mesas')

@user_passes_test(es_cocinero)
def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'Pedidos.html', {"pedidos": pedidos})

@user_passes_test(es_cocinero)
def cambiar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Pedido.ESTADOS).keys():
            pedido.estado = nuevo_estado
            pedido.save()
    return redirect('pedidos')

@user_passes_test(es_camarero)
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

@user_passes_test(es_admin)
def eliminar_cuenta(request, usuario_id):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.delete()
        return redirect('cuentas')  # Reemplaza con el nombre de tu URL de listado
    return redirect('cuentas')

@user_passes_test(es_admin)
def modificar_cuenta(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        # Procesar el formulario de modificación
        form = RegistroAdminFormulario(request.POST, instance=usuario)
        if form.is_valid():
            usuario_nuevo = form.save(commit=False)
            usuario_nuevo.set_password(form.cleaned_data['password'])
            usuario_nuevo.save()
            return redirect('cuentas')
    else:
        form = RegistroAdminFormulario(instance=usuario)

    return render(request, 'AdminModificarCuenta.html', {
        'form': form,
        'usuario': usuario
    })



@login_required
def personalizar(request):
    if request.method == 'POST':
        form = PersonalizarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            usuario_nuevo = form.save(commit=False)
            usuario_nuevo.set_password(form.cleaned_data['password'])
            usuario_nuevo.save()
            return redirect('home')
    else:
        form = PersonalizarForm(instance=request.user)

    return render(request, 'Personalizacion.html', {'form': form})

@user_passes_test(es_admin)
def añadir_producto(request):
    if request.method == 'POST':
        form = ProductoAdminFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AdminCarta')
    else:
        form = ProductoAdminFormulario()

    return render(request, "AñadirProducto.html", {'form': form})

@user_passes_test(es_admin)
def agregar_mesa(request):
    ultima_mesa = Mesa.objects.order_by('-numero').first()
    nuevo_numero = (ultima_mesa.numero + 1) if ultima_mesa else 1

    Mesa.objects.create(
        numero=nuevo_numero,
        estado='DISPONIBLE'
    )
    return redirect('AdminMesas')

@user_passes_test(es_admin)
def eliminar_mesa(request):
    ultima_mesa = Mesa.objects.order_by('-numero').first()
    if ultima_mesa:
        numero = ultima_mesa.numero
        ultima_mesa.delete()

    return redirect('AdminMesas')

#CARTA Y PEDIDOS

def cargar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Carta-LogIn.html', {'productos': productos})

@user_passes_test(es_admin)
def eliminar_producto(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
    return redirect('AdminCarta')

@user_passes_test(es_admin)
def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoAdminFormulario(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('AdminCarta')
    else:
        form = ProductoAdminFormulario(instance=producto)

    return render(request, 'AñadirProducto.html', {
        'form': form,
        'producto': producto,
    })

@user_passes_test(es_camarero)
def carta(request):
    productos = Producto.objects.all()
    carrito = Carrito.objects.filter(cliente=request.user, activo=True).first()
    mesas = Mesa.objects.filter(estado='OCUPADA')
    clientes = Usuario.objects.filter(rol='cliente')
    return render(request, 'CartaPedir.html', {'productos': productos, 'carrito': carrito, 'mesas': mesas, 'clientes': clientes})

@user_passes_test(es_camarero)
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

@user_passes_test(es_camarero)
def eliminar_item_carrito(request, item_id):
    item = ItemCarrito.objects.get(id=item_id)
    if item.carrito.cliente == request.user:
        item.delete()
    return redirect('carta_pedir')

@user_passes_test(es_camarero)
def hacer_pedido(request):
    if request.method == 'POST':
        carrito = Carrito.objects.filter(cliente=request.user, activo=True).first()
        mesa_id = request.POST.get('mesa_id')
        cliente_id = request.POST.get('cliente_id')
        mesa = get_object_or_404(Mesa, id=mesa_id)

        if not carrito or not carrito.items.exists():
            return redirect('cartapedir')

        # Obtener cliente si se seleccionó uno
        cliente = None
        if cliente_id:
            cliente = get_object_or_404(Usuario, id=cliente_id)

        # Crear pedido
        pedido = Pedido.objects.create(
            camarero=request.user,  # El usuario actual es el camarero
            cliente=cliente,        # Puede ser None si no se selecciona cliente
            mesa=mesa,
            total=carrito.total
        )

        # Copiar ítems del carrito al pedido
        for item in carrito.items.all():
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )

        # Vaciar el carrito
        carrito.items.all().delete()
        carrito.activo = False
        carrito.save()

        return redirect('carta_pedir')

    return redirect('cartapedir')


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

def registrar_usuario_admin(request):
    form = RegistroAdminFormulario()
    if request.method == 'POST':
        form = RegistroAdminFormulario(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save(commit=False)
            usuario_nuevo.set_password(form.cleaned_data['password'])
            usuario_nuevo.save()
            return redirect( 'cuentas' )
    else:
        return render(request,"AdminRegistrar.html", {'form':form})
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