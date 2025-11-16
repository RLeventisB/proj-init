from django.contrib.auth import hashers

from GestionPerfil.models import Usuarios
from GestionPosts.models import Comentarios
from GestionPosts.models import ComentarioBorrado


# omg tipos especificados??? en mi python???? es mas probable de lo que crees.
def obtener_usuario_sesion(request) -> Usuarios:
    return Usuarios.objects.get(correo=request.session['usuario_pk'][0])


def verificar_creador(request) -> bool:
    return 'usuario_pk' in request.session and obtener_usuario_sesion(request).rango in [1, 2]


def verificar_admin(request) -> bool:
    return 'usuario_pk' in request.session and obtener_usuario_sesion(request).rango == 2


def verificar_sesion(request) -> bool:
    return 'usuario_pk' in request.session


def asignar_usuario(request, usuario) -> None:
    if usuario is None and 'usuario_pk' in request.session:
        del request.session['usuario_pk']
        del request.session['usuario']

        return

    request.session['usuario_pk'] = usuario.correo, usuario.nombre
    request.session['usuario'] = usuario.nombre


# gracias django por ser open source
# basado en AbstractBaseUser.set_password el cual llama hashers.make_password
def encriptar_contraseña(contraseña: str):
    return hashers.make_password(contraseña)


def borrar_comentario(comentario: Comentarios):
    registro = ComentarioBorrado(correo=comentario.correo, contenido=comentario.contenido)
    registro.save()
    comentario.delete()
