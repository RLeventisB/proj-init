from django.db import models
from martor.models import MartorField

from GestionPerfil.models import Usuarios


# Create your models here.

class Tags(models.Model):
    contenido = models.CharField(max_length=15)

    # NO CONVERTIR A LLAVE PRIMARIA porfavor los ManyToManyFields requieren ids pq las bases de dato estan bien hechas :)

    def __str__(self):
        return self.contenido


class Publicaciones(models.Model):
    titulo = models.CharField(max_length=100)
    nombre = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    resumen = models.CharField(max_length=500)
    parrafo = MartorField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True, related_name="tag", related_query_name="tag")

    def __str__(self):
        return self.titulo


class Comentarios(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    correo = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario by {self.correo} on {self.publicacion}'
