from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        try:
            usuario = Usuarios.objects.get(correo=correo, contraseña=contraseña)
            return redirect('home')
        except Usuarios.DoesNotExist:
            return HttpResponse('Credenciales inválidas. Inténtalo de nuevo.')
    return render(request, 'login.html', {'form': LoginForm})
