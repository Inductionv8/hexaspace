from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from game.models import *
# Create your views here.

def pagina_principal(request):
    """
    Pagina principal, con posibilidad de ingresar un nombre de 
    usuario para empezar a jugar. Si el nombre de usuario existe
    entonces le muestra un mensaje de alerta.
    """
    return render_to_response('main.html')

def registrar_usuario(request):
    if not 'usuario_text' in request.GET:
        return render_to_response('registrar_usuario.html')

    nombre_usuario = request.GET.get('usuario_text')
    password_usuario = request.GET.get('password_text')
    
    # Vemos si el nombre de usuario ya existe.
    if not User.objects.filter(username=nombre_usuario).exists():
        usuario = User.objects.create_user(nombre_usuario, "", password_usuario)
        usuario.save()
    else:
        mensaje = "El nombre de usuario ya existe"
        return render_to_response('registrar_usuario.html',{'mostrar_mensaje':mensaje})

    return HttpResponseRedirect('/')
    
def loguear_usuario(request):
    """
        Se puede ingresar a esta view a traves del hipervinculo en el main.html
        o porque el usuario a hecho clicl en 'aceptar' dentro de la pagina del
        login.
    """
    # Vemos si se ingreso al logueo.
    if not 'usuario' in request.GET:
        state = "Por favor, ingrese nombre de usuario y clave."
        return render_to_response('loguear_usuario.html',{'state':state})
    # Ahora veamos si el usuario ingreso nombre de usuario y clave.
    if not 'clave' in request.GET:
        state = "Por favor ingrese la clave."
        return render_to_response('loguear_usuario.html',{'state':state})
    # Autenticamos al usuario.
    usuario = request.GET.get('usuario')
    clave = request.GET.get('clave')
    user = authenticate(username=usuario, password=clave)
    # Logueamos al usuario siempre y cuando se haya autenticado.
    if user is not None:
        if user.is_active:
            login(request,user)
    return HttpResponseRedirect("/sala_de_partidas/")

def sala_de_partidas(request):
    user = get_user(request)
    lista_partidas = []     # Es un array de array de Jugadores --> [[jugadores]]
    if 'max_cantidad_jugadores' in request.GET:
        # Creo Partida
        nueva_partida = Partida()
        nueva_partida.save()
        # Obtener el Usuario actual       
        jugador = Jugador(partida_id=nueva_partida,usuario_id=user,nombre=user.username)
        jugador.save()
    # Creamos una lista de partidas que se mostrara en la sala de partidas.
    for partida in list(Partida.objects.all()):
        lista_partidas.append(list(Jugador.objects.filter(partida_id=partida)))

    return render_to_response('sala_de_partidas.html', {'lista_partidas':lista_partidas})
