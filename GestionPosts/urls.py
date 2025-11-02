from django.urls import path
from . import views

urlpatterns = [
    path('crearpost/', views.crearpost, name='crearpost'),
    path('gestionarposts', views.gestionposts, name='gestionarposts'),
    path('post/<int:pk>/', views.post, name='post'),
    path('comentario/<int:pk>/', views.eliminarcomentarios, name='eliminar'),
]
