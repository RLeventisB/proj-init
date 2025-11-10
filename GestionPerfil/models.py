from django.contrib.auth import hashers
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

    # gracias django por ser open source
    # basado en AbstractBaseUser.set_password el cual llama hashers.make_password
    # asignar contraseña no debe de ser usado afuera >:(
    def contraseña_valida(self, contraseña):
        return hashers.check_password(contraseña, self.contraseña, self.asignar_contraseña)

    def cambiar_contraseña(self, contraseña_nueva):
        self.asignar_contraseña(hashers.make_password(contraseña_nueva))

    def asignar_contraseña(self, contraseña_encriptada):
        self.contraseña = contraseña_encriptada
        self.save(update_fields=["contraseña"])
