from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from GestionPosts.forms import CommentForm
from GestionPerfil.models import Usuarios
from GestionPosts.forms import PostForm
from .models import Publicaciones, Comentarios, Tags
from miapp import utils


# Create your views here.
def crearpost(request: WSGIRequest):
    if not utils.verificar_creador(request):
        # vete de aqui >:(
        return redirect('../')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if 'publish' in request.POST:
            # VAMOOOOOOOOO ME LEI https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/
            # ModelForm tiene un misterioso 2do parametro no borrar o si no no habran imagenes
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
        elif 'addtag' in request.POST:
            # is_bound es un booleano que dice si se ha modificado el formulario y sirve para evitar procesarlo (y mostrar los errores)
            # como se dio a un boton que no modifica el formulario, no molestar el creador con advertencias falsas y no mostrar los errores lol
            # todo: oh no como es un form aparte no se guardan los datos del form del post y se pierde todo el progreso quiero dormir
            form.is_bound = False

            datos_post = request.POST.getlist('addtag')
            if len(datos_post) > 0:
                contenido_tag_nuevo = datos_post[0].lower()
                if not Tags.objects.filter(contenido=contenido_tag_nuevo).exists() and len(contenido_tag_nuevo) > 0:
                    tag_nuevo = Tags(contenido=contenido_tag_nuevo)
                    tag_nuevo.save()
                    # form['tags'].add(tag_nuevo)

    else:
        form = PostForm()

    # TODO: markdown deja procesar imagenes, idealmente se deben de procesar las imagenes
    # hit da books https://django-markdown-editor.readthedocs.io/en/latest/settings.html#image-upload-configuration
    return render(request, 'crearpost.html', context={'form': form})


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
