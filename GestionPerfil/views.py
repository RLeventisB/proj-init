from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from GestionPosts.models import Comentarios
from miapp import utils
from .forms import SignupForm
from .forms import LoginForm
from .forms import UserUpdateForm
from .models import Usuarios


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            usuario = Usuarios.objects.get(correo=form.instance.correo)

            request.session['usuario_pk'] = usuario.correo, usuario.nombre
            request.session['usuario'] = usuario.nombre

            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and Usuarios.objects.filter(correo=form.cleaned_data['correo'],
                                                       contraseña=form.cleaned_data['contraseña']).exists():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuarios.objects.get(correo=correo)
            if usuario.contraseña == contraseña:
                utils.asignar_usuario(request, usuario)

                return redirect('home')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    utils.asignar_usuario(request, None)

    return redirect('home')


def formulariosperfil(request):
    if not utils.verificar_sesion(request):
        # vete de aqui >:(
        return redirect('../')

    nameupdateform = UserUpdateForm(request.POST)
    usuario = utils.obtener_usuario_sesion(request)

    if request.method == 'POST':
        if 'solicitar_cambio_usuario' in request.POST:
            if nameupdateform.is_valid():
                nombre_nuevo = nameupdateform.cleaned_data['nombre']
                usuario.nombre = nombre_nuevo
                usuario.save()

                utils.asignar_usuario(request, usuario)

                return redirect('perfil')
            pass

        if 'crear_post' in request.POST:
            return redirect('crearpost')

        if 'ver_posts' in request.POST:
            return redirect('gestionarposts')

        if 'ver_comentarios' in request.POST:
            return redirect('ver_comentarios')

        elif 'borrar_cuenta' in request.POST:
            try:
                usuario.delete()
                utils.asignar_usuario(request, None)

                return redirect('home')

            except usuario.DoesNotExist:
                return redirect('perfil')

    es_creador = usuario.rango != 0
    return render(request, 'perfil.html', {
        'nameupdateform': nameupdateform,
        'es_creador': es_creador})


def obtener_comentario(usuario: Usuarios, index: int) -> Comentarios:
    comentario = Comentarios.objects.get(id=index)
    if usuario.rango == 2 or comentario.correo == usuario:
        return comentario
    raise AssertionError("Acceso denegado")


def gestioncomentarios(request: WSGIRequest):
    if not utils.verificar_sesion(request):
        # vete de aqui >:(
        return redirect('../')

    usuario = utils.obtener_usuario_sesion(request)

    if 'accion' in request.GET and 'id' in request.GET:
        # oh no estamos en presencia de una ACCION!!!
        try:
            accion = request.GET.get('accion')
            index = int(request.GET.get('id'))
            comentario = obtener_comentario(usuario, index)
            if accion == 'borrar':
                comentario.delete()
            if accion == 'editar':
                # blehhhhhh
                pass
        finally:
            # redirect para borrar los parametros
            return redirect('ver_comentarios')

    comentarios = Comentarios.objects.filter(correo=usuario).all()

    return render(request, 'gestioncomentario.html', context={'resultados': comentarios, 'nombre_plural': "Comentarios", 'admin': usuario.rango == 2})
