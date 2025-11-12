import json
import os
import uuid

from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from martor.utils import LazyEncoder

from GestionPerfil.models import Usuarios
from GestionPosts.forms import CommentForm
from GestionPosts.forms import PostForm
from config import settings
from miapp import utils
from .models import Publicaciones, Comentarios, Tags


# Create your views here.
def añadirtag(request: WSGIRequest):
    # view para cuando le den al boton de añadir tags
    # si el tag tiene un tamaño mayor a 0, y no existe uno en minuscula, decimos tag aceptado!!! (202) si no solo ok :)

    if 'tag' in request.GET:
        tag_a_añadir = request.GET['tag']
        if len(tag_a_añadir) > 0:
            contenido_tag_nuevo = tag_a_añadir.lower()
            if not Tags.objects.filter(contenido=contenido_tag_nuevo).exists():
                tag_nuevo = Tags(contenido=contenido_tag_nuevo)
                tag_nuevo.save()

                data = json.dumps({
                    'id': tag_nuevo.id,  # esto se usa en el html,,
                    'contenido': contenido_tag_nuevo,
                    'status': 202,  # 202 significa lo aceptamos!!!
                })
                return HttpResponse(data, content_type='application/json')

    data = json.dumps({
        'status': 200,
    })
    return HttpResponse(data, content_type='application/json')


def crearpost(request: WSGIRequest):
    if not utils.verificar_creador(request):
        # vete de aqui >:(
        return redirect('../')

    if request.method == 'POST':
        # VAMOOOOOOOOO ME LEI https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/
        # ModelForm tiene un misterioso 2do parametro no borrar o si no no habran imagenes
        form = PostForm(request.POST, request.FILES)

        if 'publish' in request.POST:
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
        if 'tag' in request.GET:
            return añadirtag(request)

        form = PostForm()

    return render(request, 'crearpost.html', context={'form': form})


def post(request, pk):
    post: Publicaciones = get_object_or_404(Publicaciones, pk=pk)
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


def obtener_post(usuario: Usuarios, index: int) -> Publicaciones:
    post = Publicaciones.objects.get(id=index)
    if usuario.rango == 2 or post.nombre == usuario:
        return post
    raise AssertionError("Acceso denegado")


def gestionposts(request: WSGIRequest):
    if not utils.verificar_creador(request):
        # vete de aqui >:(
        return redirect('../')

    usuario = utils.obtener_usuario_sesion(request)

    if 'accion' in request.GET and 'id' in request.GET:
        # oh no estamos en presencia de una ACCION!!!
        try:
            accion = request.GET.get('accion')
            index = int(request.GET.get('id'))
            post = obtener_post(usuario, index)
            if accion == 'borrar':
                post.delete()
            if accion == 'editar':
                # blehhhhhh
                pass
        finally:
            # redirect para borrar los parametros
            return redirect('gestionarposts')

    if usuario.rango == 2:
        publicaciones = Publicaciones.objects.all()
    else:
        publicaciones = Publicaciones.objects.filter(nombre=usuario).all()

    return render(request, 'gestionpost.html',
                  context={'resultados': publicaciones, 'nombre_plural': "Publicaciones", 'admin': usuario.rango == 2})


def subirimagen(request: WSGIRequest):
    # basicamente copiado de https://github.com/agusmakmun/django-markdown-editor/wiki#create-custom-uploader
    # en resumen checkea si archivo es png / jpg / jpeg / gif, checkea tamaño maximo, y lo guarda
    # ah si los _("texto") son cosos para traducir pero esta pagina como que solo sera para gente española (exclusion??? en mi pagina de inclusion????)

    if request.method != 'POST':
        return HttpResponse(_('Invalid request!'))

    if 'markdown-image-upload' not in request.FILES:
        return HttpResponse(_('Invalid request!'))

    image = request.FILES['markdown-image-upload']
    image_types = [
        'image/png', 'image/jpg',
        'image/jpeg', 'image/pjpeg', 'image/gif'
    ]
    if image.content_type not in image_types:
        data = json.dumps({
            'status': 405,
            'error': _('Bad image format.')
        }, cls=LazyEncoder)
        return HttpResponse(
            data, content_type='application/json', status=405)

    if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
        to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
        data = json.dumps({
            'status': 405,
            'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}
        }, cls=LazyEncoder)
        return HttpResponse(
            data, content_type='application/json', status=405)

    img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
    tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
    def_path = default_storage.save(tmp_file, ContentFile(image.read()))
    img_url = os.path.join(settings.MEDIA_URL, def_path)

    data = json.dumps({
        'status': 200,
        'link': img_url,
        'name': image.name
    })
    return HttpResponse(data, content_type='application/json')
