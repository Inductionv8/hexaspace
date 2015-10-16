from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from game.models import *
# Create your views here.

def homepage(request):
    """
    Si hay algun usuario, lo redirige a la homepage para que se loguee.
    """
    return render_to_response('main.html')

def lobby(request):
    state = "No hay estado"
    usuario = ""
    if 'usuario' in request.GET:
        usuario = request.GET.get('usuario')
        jugador = Jugador()
        jugador.nombre = usuario
        state = jugador.nombre
    elif 'crear' in request.GET:
        state = "EL JUGADOR QUIZO CREAR JAJA"
    return render_to_response('lobby.html',{'state':state})
