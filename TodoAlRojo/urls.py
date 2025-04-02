from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', go_home_page, name='home'),
    path('home/', go_home_page , name="home"),
]