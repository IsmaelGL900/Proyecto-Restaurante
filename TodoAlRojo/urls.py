from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', go_home_page , name="home"),
    path('', logout_usuario, name="logout"),
    path('home/', go_homeLogIn_page, name="home-login"),
    path('home/carta/', cargar_productos, name="carta_LogIn"),
    path('home/historial/', go_historial_page, name="historial"),
    path('home/personalizacion/', personalizar, name="personalizar"),
    path('carta/', carta_SinCuenta, name="carta_SinCuenta"),
    path('cartapedir/', carta, name='carta_pedir'),
    path('cartapedir/agregar-a-carrito/<int:producto_id>/', agregar_a_carrito, name='agregar_a_carrito'),
    path('cartapedir/eliminar-item-carrito/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
    path('cartapedir/pedidos/', go_pedidoscamarero_page, name="pedidosCamarero"),
    path('cartapedir/pedidos/editar/<int:pedido_id>/', editar_pedido, name="editar_pedido"),
    path('hacer-pedido/', hacer_pedido, name='hacer_pedido'),
    path('pedidos/', pedidos, name='pedidos'),
    path('pedidos/cambiar_estado/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('PedidosAdmin/', ver_pedidos, name='pedidos_admin'),

    path('GestionCamarero/Mesas/', cargarTablaMesas, name='mesas'),
    path('GestionCamarero/Mesas/cobrar/<int:mesa_id>/', views.cobrar_mesa, name='cobrar_mesa'),
    path('GestionCamarero/Mesas/cambiar-estado/<int:mesa_id>/', cambiar_estado, name='cambiar_estado'),
    path('login/', loguearse, name="login"),
    path('login/registrarse/',registrar_usuario, name="registrarse"),
    path('logout/', logout_usuario, name='logout'),
    path('GestionCocinero/', go_GestionCocinero_page, name="GestionCocinero"),
    path('GestionCamarero/', go_GestionCamarero_page , name="GestionCamarero"),
    path('GestionAdministrador/', go_GestionAdministrador_page, name="GestionAdmin"),
    path ('GestionAdministrador/AdministrarMesas/', go_AdminMesas_page, name="AdminMesas"),
    path('GestionAdministrador/AdministrarMesas/agregar/', views.agregar_mesa, name='agregar_mesa'),
    path('GestionAdministrador/AdministrarMesas/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),
    path('GestionAdministrador/AdminCarta/', go_AdminCarta_page, name="AdminCarta"),
    path('GestionAdministrador/AdminCarta/AñadirProducto', añadir_producto, name="AñadirProducto"),
    path('GestionAdministrador/AdminCarta/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('GestionAdministrador/AdminCarta/modificar/<int:producto_id>/', views.modificar_producto, name='modificar_producto'),
    path('GestionAdministrador/Cuentas/', go_cuentas_page, name="cuentas"),
    path('GestionAdministrador/Cuentas/eliminar-cuenta/<int:usuario_id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('GestionAdministrador/Cuentas/modificar-cuenta/<int:usuario_id>/', views.modificar_cuenta, name='modificar_cuenta'),
    path('GestionAdministrador/Cuentas/registrarse/',registrar_usuario_admin, name="registrarse_admin"),
]