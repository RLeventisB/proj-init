from django.urls import path
from . import views

urlpatterns = [
    path('crearpost/', views.crearpost, name='crearpost'),
    path('post/<int:pk>/', views.post, name='post'),
]
