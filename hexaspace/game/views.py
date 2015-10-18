from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from game.models import *
# Create your views here.

def homepage(request):
    """
    Pagina principal, con posibilidad de ingresar un nombre de 
    usuario para empezar a jugar. Si el nombre de usuario existe
    entonces le muestra un mensaje de alerta.
    """
    state = "Bienvenido a HexaSpace."
    print get_user(request)          #Debugging Line
    if 'usuario' in request.GET:
        usuario = request.GET.get('usuario')
        if not User.objects.filter(username=usuario).exists():
            user = User.objects.create_user(usuario, "", "")
            user.save()
            myuser = authenticate(username=usuario, password="")
            # Init Debugging Lines
            if myuser is not None:
                print "ENTROOO!"
                if myuser.is_active:
                    print "ESACITVO"
                    login(request, myuser)
            # End Debugging Lines
            return HttpResponseRedirect('lobby')
        else:
            state = "El nombre de usuario ya existe. Elije otro."
    return render_to_response('main.html',{'state':state})

def lobby(request):
    user = get_user(request)
    print "user en lobby:"
    print user
    if 'crear' in request.GET:
        # Creo Partida
        nueva_partida = Partida()
        nueva_partida.save()
        # Obtener el Usuario actual       
        jugador = Jugador(partida_id=nueva_partida,usuario_id=user,nombre=user.username)
        jugador.save()
    return render_to_response('lobby.html',{'NombreUsuario':user.username})
