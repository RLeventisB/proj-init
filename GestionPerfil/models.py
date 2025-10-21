from django.db import models

# Create your models here.

class Usuarios(models.Model):
    correo = models.EmailField(primary_key=True)
    nombre = models.CharField(max_length=15)
    contraseña = models.CharField(max_length=10)
    contraseña2 = models.CharField(max_length=10, default=contraseña)
    rango = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre
    