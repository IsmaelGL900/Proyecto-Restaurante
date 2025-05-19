from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', go_home_page , name="home"),
    path('', logout_usuario, name="logout"),
    path('home/', go_homeLogIn_page, name="home-login"),
    path('home/carta', cargar_productos, name="carta"),
    path('cartapedir/', carta, name='carta_pedir'),
    path('cartapedir/agregar-a-carrito/<int:producto_id>/', agregar_a_carrito, name='agregar_a_carrito'),
    path('cartapedir/eliminar-item-carrito/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
    path('hacer-pedido/', hacer_pedido, name='hacer_pedido'),


    path('GestionCamarero/Mesas/', cargarTablaMesas, name='mesas'),
    path('GestionCamarero/Mesas/cambiar-estado/<int:mesa_id>/', cambiar_estado, name='cambiar_estado'),
    path('login/', loguearse, name="login"),
    path('login/registrarse/',registrar_usuario, name="registrarse"),
    path('logout/', logout_usuario, name='logout'),
    path('GestionCocinero/', go_GestionCocinero_page, name="GestionCocinero"),
    path('GestionCamarero/', go_GestionCamarero_page , name="GestionCamarero"),
    path('GestionAdministrador/', go_GestionAdministrador_page, name="GestionAdmin"),
    path('GestionAdministrador/Cuentas/', go_cuentas_page, name="cuentas"),
    path('GestionAdministrador/Cuentas/registrarse/',registrar_usuario_admin, name="registrarse_admin"),
]