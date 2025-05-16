from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', go_home_page , name="home"),
    path('', logout_usuario, name="logout"),
    path('home/', go_homeLogIn_page, name="home-login"),
    path('home/carta', go_carta_page, name="carta"),
    path('GestionCamarero/Mesas/', cargarTablaMesas, name='mesas'),
    path('GestionCamarero/Mesas/cambiar-estado/<int:mesa_id>/', cambiar_estado, name='cambiar_estado'),
    path('login/', loguearse, name="login"),
    path('login/registrarse/',registrar_usuario, name="registrarse"),
    path('logout/', logout_usuario, name='logout'),
    path('GestionCocinero/', go_GestionCocinero_page, name="GestionCocinero"),
    path('GestionCamarero/', go_GestionCamarero_page , name="GestionCamarero"),
    path('GestionAdministrador/', go_GestionAdministrador_page, name="GestionAdmin"),


]