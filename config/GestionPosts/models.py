from django.db import models
from GestionPerfil.models import Usuarios

# Create your models here.

class Tags(models.Model):
    tag = models.CharField(max_length=15, primary_key=True)

    def __str__(self):
        return self.tag
    
class Publicaciones(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=40)
    nombre = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    resumen = models.CharField(max_length=500)
    parrafo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.titulo
    
class Comentarios(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    correo = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario by {self.correo} on {self.publicacion}'

