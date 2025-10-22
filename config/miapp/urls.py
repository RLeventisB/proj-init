from django.urls import path,include  
from django.contrib import admin
from . import views
from GestionPerfil.urls import urlpatterns as gestionperfil_urls
from GestionPerfil.views import *


urlpatterns = [
    path('', views.home, name='home'),
    path('GestionPerfil/login', include(gestionperfil_urls), name='login'),
    path('GestionPerfil/signup', include(gestionperfil_urls), name='signup'),
]