import datetime

from django.shortcuts import render, redirect, get_object_or_404

from GestionPerfil.models import Usuarios
from GestionPosts.forms import PostForm
from .models import Publicaciones


def verificar_sesion(request):
    return 'usuario_pk' in request.session and Usuarios.objects.get(correo=request.session['usuario_pk'][0]).rango != 0


# Create your views here.
def crearpost(request):
    if not verificar_sesion(request):
        # vete de aqui >:(
        return redirect('../')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            usuario = Usuarios.objects.get(correo=request.session['usuario_pk'][0])
            if usuario.rango == 0:
                return redirect('../')

            form.instance.nombre = usuario
            publicacion = form.save()

            # se tiene que guardar el forms primero para generar la id, y asi los tags pueden tener una llave primaria a la cual se enlazan, yipee.

            for tagSeleccionado in form.cleaned_data.get('tags'):
                publicacion.tags.add(tagSeleccionado)
            publicacion.save()

            return redirect('perfil')
    else:
        form = PostForm()

    return render(request, 'crearpost.html', context={'form': form, 'sobreescribir_css': True})

def post(request, pk):
    post = get_object_or_404(Publicaciones, pk=pk)
    return render(request, 'post.html', {'post': post})