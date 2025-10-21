from django.shortcuts import render, redirect
from .forms import CuestionarioForm
from .forms import LoginForm
from .models import Usuarios

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CuestionarioForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and Usuarios.objects.filter(correo=form.cleaned_data['correo'], contraseña=form.cleaned_data['contraseña']).exists():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuarios.objects.get(correo=correo)
            if usuario.contraseña == contraseña:
                request.session['usuario_pk'] = usuario.correo
                return redirect('home')
        else:
            return render(request, 'login.html', {'form': form})
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