from GestionPerfil.models import Usuarios


# omg tipos especificados??? en mi python???? es mas probable de lo que crees.
def obtener_usuario_sesion(request) -> Usuarios:
    return Usuarios.objects.get(correo=request.session['usuario_pk'][0])


def verificar_creador(request) -> bool:
    return 'usuario_pk' in request.session and obtener_usuario_sesion(request).rango in [1, 2]


def verificar_sesion(request) -> bool:
    return 'usuario_pk' in request.session


def asignar_usuario(request, usuario) -> None:
    if usuario is None and 'usuario_pk' in request.session:
        del request.session['usuario_pk']

        return
    
    request.session['usuario_pk'] = usuario.correo, usuario.nombre

    # usamos esto???????
    # request.session['usuario'] = usuario.nombre
