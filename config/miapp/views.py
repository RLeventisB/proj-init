from django.shortcuts import render
from .forms import*
from .models import*
from GestionPosts.models import Publicaciones


# Create your views here.
def home(request):
    # todo: esto es ineficiente porfavor hagan un comando para sqlite donde se obtienen los primeros 3 en vez de allocar toda la santa base de datos.
    moriras = Publicaciones(id=1,
    titulo= 'CONCJEGTIMARE',
    resumen="ade",
    parrafo="moriras"
    )
    # tienetexto = Publicaciones.objects.order_by("fecha_creacion").all()[:3]
    tienetexto = {
        "publicaciones":[moriras]
    }
    return render(request,'home.html', context=tienetexto)
def perfil(request):
    return render(request, 'perfil.html')
def login(request):
    return render(request,'login.html' )

