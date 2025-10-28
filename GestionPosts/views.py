from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from GestionPosts.forms import CommentForm
from GestionPerfil.models import Usuarios
from GestionPosts.forms import PostForm
from .models import Publicaciones, Comentarios
from miapp import utils


# Create your views here.
def crearpost(request):
    if not utils.verificar_creador(request):
        # vete de aqui >:(
        return redirect('../')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            usuario = utils.obtener_usuario_sesion(request)
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
    comments = Comentarios.objects.filter(publicacion=post)
    autenticado = utils.verificar_sesion(request)
    context = {
        "post": post,
        "comments": comments,
        "autenticado": autenticado
    }

    if autenticado:
        context["usuario_actual"] = utils.obtener_usuario_sesion(request)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                usuario = utils.obtener_usuario_sesion(request)
                comment = Comentarios(
                    contenido=form.cleaned_data['body'],
                    publicacion=post,
                    correo=usuario,
                )
                comment.save()
                form = CommentForm()
                context["form"] = form

                # redirect ya que https://stackoverflow.com/a/14534547
                return redirect('.', context)

        else:
            form = CommentForm()

        context["form"] = form

    return render(request, 'post.html', context)

def eliminarcomentarios(request, pk):
    instance = get_object_or_404(Comentarios, pk=pk)
    if instance.correo != utils.obtener_usuario_sesion(request):
        response = HttpResponse("No tienes permitido realizar esta acción")
        response.status_code = 403
        return response
    
    if request.method == "POST":
        padre_instance_url = instance.publicacion.get_absolute_url()
        instance.delete()
        messages.success(request, "Se ha eliminado tu comentario")
        return HttpResponseRedirect(padre_instance_url)
    
    context = {
        'instance': instance
    }
    return render(request, 'eliminar.html', context)
