from django.db import models

# Create your models here.

class Usuarios(models.Model):
    correo = models.EmailField(primary_key=True)
    nombre = models.CharField(max_length=15)
    contraseña = models.CharField(max_length=10)
    rango = models.IntegerField()

    def __str__(self):
        return self.nombre
