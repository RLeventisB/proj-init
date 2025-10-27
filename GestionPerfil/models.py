from django.db import models

# Create your models here.
RANGOS = {
    0: "Visitante",
    1: "Creador",
    2: "Admin"
}

class Usuarios(models.Model):
    correo = models.EmailField(primary_key=True)
    nombre = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=100)
    rango = models.IntegerField(default=0, choices=RANGOS)

    def __str__(self):
        return self.nombre
    