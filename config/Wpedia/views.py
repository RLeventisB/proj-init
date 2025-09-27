from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    contexto = {
        'texto': "Bienvenido a la página principal de Wpedia"
    }
    return render(request, 'home.html', contexto)
