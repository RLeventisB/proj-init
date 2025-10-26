from django.shortcuts import render
from .forms import*
from .models import*
from GestionPosts.models import Publicaciones

# Create your views here.
def home(request):
    publicaciones = list(Publicaciones.objects.order_by("fecha_creacion").all()[:3])
    return render(request,'home.html', context={
        "publicaciones":publicaciones
    })
def perfil(request):
    return render(request, 'perfil.html')
def login(request):
    return render(request,'login.html' )

