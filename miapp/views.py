from django.shortcuts import render
from .forms import *
from .models import *
from GestionPosts.models import Publicaciones


# Create your views here.
def home(request):
    publicaciones = Publicaciones.objects.order_by("fecha_creacion").all().reverse()[:3]
    return render(request, 'home.html', context={
        "publicaciones": publicaciones
    })
