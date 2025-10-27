from django.shortcuts import render, redirect

import GestionPerfil.models
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
                request.session['usuario_pk'] = usuario.correo, usuario.nombre
                request.session['usuario'] = usuario.nombre

                return redirect('home')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def verificar_sesion(request):
    return 'usuario_pk' in request.session


def logout(request):
    if 'usuario_pk' in request.session:
        del request.session['usuario_pk']
    return redirect('home')


def formulariosperfil(request):
    if not verificar_sesion(request):
        # vete de aqui >:(
        return redirect('../')

    nameupdateform = UserUpdateForm(request.POST)
    usuario = Usuarios.objects.get(correo=request.session['usuario_pk'][0])

    if request.method == 'POST':
        if 'solicitar_cambio_usuario' in request.POST:
            if nameupdateform.is_valid():
                nombre_nuevo = nameupdateform.cleaned_data['nombre']
                usuario.nombre = nombre_nuevo
                usuario.save()

                request.session['usuario_pk'] = usuario.correo, usuario.nombre
                request.session['usuario'] = usuario.nombre

                return redirect('perfil')
            pass

        if 'crear_post' in request.POST:
            return redirect('crearpost')

        elif 'borrar_cuenta' in request.POST:
            try:
                usuario.delete()
                del request.session['usuario_pk']
                del request.session['usuario']
                return redirect('home')

            except usuario.DoesNotExist:
                return redirect('perfil')

    es_creador = usuario.rango != 0
    return render(request, 'perfil.html', {
        'nameupdateform': nameupdateform,
        'es_creador': es_creador})
