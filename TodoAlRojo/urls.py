from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('home/', go_home_page , name="home"),
    path('mesas/', go_mesas_page, name='mesas'),
    path('home/login/', go_login_page, name="login"),
    path('home/login/registrarse/', go_registrarse_page, name="registrarse"),
    path('gestion/', go_gestion_page, name="gestion"),
    path('gestion/loginCocinero/', go_loginCocinero_page, name="loginCocinero"),
    path('gestion/loginCamarero/', go_loginCamarero_page , name="loginCamarero"),
    path('gestion/loginAdministrador/', go_loginAdministrador_page, name="loginAdministrador"),
]