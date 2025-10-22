from django.shortcuts import render
from .forms import*
from .models import*
from GestionPosts.models import Publicaciones
from GestionPerfil.views import signup

# Create your views here.
def home(request):
    # todo: esto es ineficiente porfavor hagan un comando para sqlite donde se obtienen los primeros 3 en vez de allocar toda la santa base de datos.
    nomegusta = Publicaciones(id=1,
    titulo= 'Safe and Sound',
    resumen="ade",
    parrafo="PEP 8: E128 continuation line under-indented for visual indent"
    )
    # tienetexto = Publicaciones.objects.order_by("fecha_creacion").all()[:3]
    posts = {
        "publicaciones":[nomegusta]
    }
    return render(request,'home.html', context=posts)
def perfil(request):
    return render(request, 'perfil.html')
def login(request):
    return render(request,'login.html' )
def singup(request):
    return signup(request,'GestionPerfil/signup.html')

