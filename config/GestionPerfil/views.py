from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CuestionarioForm
from .models import Usuarios


# Create your views here.

def signup(request):
    if request.method == 'POST':
        request.POST['contraseña'] == request.POST['contraseña2']
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CuestionarioForm()
    return render(request, 'signup.html', {'form': form})
