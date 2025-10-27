from django.urls import path
from . import views

urlpatterns = [
    path('busqueda/', views.busqueda, name='busqueda'),
]