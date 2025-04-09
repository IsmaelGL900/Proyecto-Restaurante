from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('home/', go_home_page , name="home"),
    path('mesas/', go_mesas_page, name='mesas'),
    path('home/login/', go_login_page, name="login"),
    path('home/login/registrarse/', go_registrarse_page, name="registrarse"),
]