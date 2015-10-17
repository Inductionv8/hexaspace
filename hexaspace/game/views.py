from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from game.models import *
# Create your views here.

def lobby_table():
    """
    Tabla con 4 jugadores de prueba para tener algo
    """
    jugador1 = Jugador()
    jugador2 = Jugador()
    jugador3 = Jugador()
    jugador4 = Jugador()
    jugador1.nombre = "PrimerJugador"
    jugador2.nombre = "SegundoJugador"
    jugador3.nombre = "TercerJugador"
    jugador4.nombre = "CuartoJugador"
    return [jugador1,jugador2,jugador3,jugador4]

def homepage(request):
    """
    Pagina principal, con posibilidad de ingresar un nombre de 
    usuario para empezar a jugar. Si el nombre de usuario existe
    entonces le muestra un mensaje de alerta.
    """
    state = "Bienvenido a HexaSpace."
    if 'usuario' in request.GET:
        usuario = request.GET.get('usuario')
        if not Jugador.objects.filter(nombre=usuario).exists():
            jugador = Jugador()
            jugador.nombre = usuario
            jugador.save()
            return HttpResponseRedirect('lobby')
        else:
            state = "El nombre de usuario ya existe. Elije otro."
    return render_to_response('main.html',{'state':state})

def lobby(request):
    state = "Cree su propia partida, o unase a alguna."
    partida = lobby_table()
    if 'crear' in request.GET:
        state = "Partida Creada, esperando oponentes."
    return render_to_response('lobby.html',{'state':state,
                                            'partida':partida
                                            })
