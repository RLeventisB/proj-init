from django.shortcuts import render
from GestionPosts.models import Publicaciones
from django.db.models import Q

# Create your views here.

def busqueda(request):
    query = request.GET.get('q')
    if query:
        publicaciones = Publicaciones.objects.filter(resumen__icontains=query)
    else:
        publicaciones = Publicaciones.objects.all()
    return render(request, 'busqueda.html', {'publicaciones': publicaciones})

