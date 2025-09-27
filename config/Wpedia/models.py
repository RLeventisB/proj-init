from django.db import models

# Create your models here.

class Usuarios(models.Model):
	usuario = models.CharField(max_length=100, primary_key=True)
	email = models.EmailField()
	contraseña = models.CharField(max_length=15)

	def __str__(self):
		return f"{self.usuario}, {self.email}"

class Informacion(models.Model):
	palabra_clave = models.CharField(max_length=20, primary_key=True) 
	titulo = models.CharField(max_length=100)
	resumen = models.CharField(max_length=500)	
	parrafo = models.TextField()

	def __str__(self):
	    return f"{self.palabra_clave}, {self.titulo}"

class Comentarios(models.Model):
	usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='usuario')
	palabra_clave = models.ForeignKey(Informacion, on_delete=models.CASCADE, to_field='palabra_clave')
	titulo = models.CharField(max_length=100)
	contenido = models.TextField(max_length=1000)

	def __str__(self):
		return f"{self.usuario}, {self.palabra_clave}, {self.titulo}"

class Likes(models.Model):
	palabra_clave = models.OneToOneField(Informacion, on_delete=models.CASCADE, to_field='palabra_clave', primary_key=True)
	recuento = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.palabra_clave} = {self.recuento}'

