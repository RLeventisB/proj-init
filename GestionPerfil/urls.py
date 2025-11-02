from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ver_comentarios/', views.gestioncomentarios, name='ver_comentarios'),
    path('perfil/', views.formulariosperfil, name='perfil'),
    path('borrar-cuenta/', views.formulariosperfil, name='borrarcuenta'),
]
