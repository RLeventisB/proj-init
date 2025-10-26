from django.urls import path
from . import views

urlpatterns = [
    path('crearpost/', views.crearpost, name='crearpost')
]
