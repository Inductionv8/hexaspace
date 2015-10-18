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
    state = "Bienvenido a HexaSpace."

    if 'usuario_text' in request.GET:
        nombre_usuario = request.GET.get('usuario_text')
        print nombre_usuario
        if not User.objects.filter(username=nombre_usuario).exists():
            usuario = User.objects.create_user(nombre_usuario, "", "")
            usuario.save()
            validated = authenticate(username=nombre_usuario, password="")
            login(request, validated)
            return HttpResponseRedirect('sala_de_partidas')
        else:
            state = "El nombre de usuario ya existe. Elije otro."
    return render_to_response('main.html',{'state':state})

def sala_de_partidas(request):
    user = get_user(request)
    if 'crear_button' in request.GET:
        # Creo Partida
        nueva_partida = Partida()
        nueva_partida.save()
        # Obtener el Usuario actual       
        jugador = Jugador(partida_id=nueva_partida,usuario_id=user,nombre=user.username)
        jugador.save()
    return render_to_response('sala_de_partidas.html',{'NombreUsuario':user.username})
