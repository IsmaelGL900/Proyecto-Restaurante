from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('home/', go_home_page , name="home"),
    path('mesas/', go_mesas_page, name='mesas'),
    path('home/login/', loguearse, name="login"),
    path('home/login/registrarse/',registrar_usuario, name="registrarse"),
    path('logout/', logout_usuario, name='logout'),
    path('gestion/', go_gestion_page, name="gestion"),
    path('gestion/loginCocinero/', go_loginCocinero_page, name="loginCocinero"),
    path('gestion/loginCamarero/', go_loginCamarero_page , name="loginCamarero"),
    path('gestion/loginAdministrador/', go_loginAdministrador_page, name="loginAdministrador"),


]