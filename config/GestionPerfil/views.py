from django.shortcuts import render, redirect
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
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and Usuarios.objects.filter(correo=form.cleaned_data['correo'], contraseña=form.cleaned_data['contraseña']).exists():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuarios.objects.get(correo=correo)
            if usuario.contraseña == contraseña:
                request.session['usuario_pk'] = usuario.correo, usuario.nombre
                request.session['usuario'] = usuario.nombre
                return redirect('home')
        else:
            return (render(request, 'login.html', {'form': form}), correo)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def verificar_sesion(request):
    if 'usuario_pk' in request.session:
        return True
    else:
        return False
    
def logout(request):
    if 'usuario_pk' in request.session:
        del request.session['usuario_pk']
    return redirect('home')
    
def formulariosperfil(request):
    form = UserUpdateForm(request.POST)
    usuario = request.session['usuario_pk'][1]
    if request.method == 'POST':
        if 'enviar_form1' in request.POST:
            if form.is_valid():
                usuario = Usuarios.objects.get(correo=request.session['usuario_pk'][0])
                usuario_nuevo = form.cleaned_data['nombre']
                usuario.nombre = usuario_nuevo
                usuario.save()
                request.session['usuario_pk'] = usuario.correo, usuario.nombre
                request.session['usuario'] = usuario.nombre
                print(request.session['usuario_pk'])
                print(request.session['usuario'])
                return redirect('perfil')
            pass
    
        elif 'borrar_cuenta' in request.POST:
            try:
                usuario = Usuarios.objects.get(correo=request.session['usuario_pk'][0])
                usuario.delete()
                del request.session['usuario_pk']
                return redirect('home')
            except usuario.DoesNotExist:
                return redirect('perfil')
            pass
    return render(request, 'perfil.html', {'form': form})
