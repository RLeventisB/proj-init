from django.shortcuts import render
from .forms import*
from .models import*
# Create your views here.
def home(request):
    return render(request,'home.html' )
def perfil(request):
    return render(request, 'perfil.html')
def login(request):
    return render(request,'login.html' )

