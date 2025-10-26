import datetime

from django.shortcuts import render, redirect

from GestionPerfil.models import Usuarios
from GestionPosts.forms import PostForm


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
            # form.instance.tags.set([])
            form.save()

            return redirect('perfil')
    else:
        form = PostForm()

    return render(request, 'crearpost.html', context={'form': form, 'sobreescribir_css': True})
