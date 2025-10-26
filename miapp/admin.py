from django.contrib import admin
from GestionPosts.models import Tags, Publicaciones, Comentarios
from GestionPerfil.models import Usuarios

# Register your models here.
admin.site.register(Tags)
admin.site.register(Publicaciones)
admin.site.register(Comentarios)
admin.site.register(Usuarios)
