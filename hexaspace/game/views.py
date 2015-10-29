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
    state = "Por favor, ingrese nombre de usuario y clave."
    # Vemos si se ingreso al logueo.
    if not 'usuario' in request.GET:
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
    state = state + " El usuario no esta registrado."
    return render_to_response('loguear_usuario.html',{'state':state})



def sala_de_partidas(request):
    """
        gid es el id de la partida a la cual se quiere unir, sera None si no hay partida.
    """
    user = get_user(request)
    lista_partidas = []     # Es un array de array de Jugadores --> [[jugadores]]
     
    if not Jugador.objects.filter(usuario_id=user).exists():
        # Aca un jugador quiere crear una partida.
        if 'max_cantidad_jugadores' in request.GET:
                nueva_partida = Partida(creador=user.username, num_max_jugadores=request.GET.get('max_cantidad_jugadores'))
                nueva_partida.save()
                # Creao al jugador en base al usuario actual
                jugador = Jugador(partida_id=nueva_partida,usuario_id=user,nombre=user.username)
                jugador.save()
                return HttpResponseRedirect("/sala_de_partidas/")

        # Ahora vemos si un jugador se quiere unir a una partida.
        if 'unirse_partida' in request.GET:
            id_partida_actual = request.GET.get('partida_a_unirse')
            partida_actual = Partida.objects.get(id=id_partida_actual) #Es la partida a la cual se quieren unir
            partida_actual.num_jugadores_actuales += 1
            partida_actual.save()
            jugador = Jugador(partida_id=partida_actual, usuario_id=user,nombre=user.username)
            jugador.save()
            return HttpResponseRedirect("/sala_de_partidas/")

    else:
        jugador = Jugador.objects.get(usuario_id=user)
        partida_del_jugador = Partida.objects.get(id=jugador.partida_id.id)
         
        # Aca el creador quiere empezar la partida.
        if "jugar" in request.GET and partida_del_jugador.creador == jugador.nombre and partida_del_jugador.num_max_jugadores == partida_del_jugador.num_jugadores_actuales:
            partida_del_jugador.partida_empezada = 1
            partida_del_jugador.save()

        # Aca entra por refresco de pagina y se lo lleva a los jugadores a la mesa de juego.
        if partida_del_jugador.partida_empezada == 1:
            url = '/mesa/{0}'.format(partida_del_jugador.id)
            return HttpResponseRedirect(url)

    #Creamos una lista de partidas que se mostrara en la sala de partidas.
    for partida in list(Partida.objects.all()):
        lista_partidas.append(list(Jugador.objects.filter(partida_id=partida)))
    return render_to_response('sala_de_partidas.html',{'lista_partidas':lista_partidas})

def mesa(request, partida_id):
    """
        Sala en la cual estara el tablero de juego.
    """
    return render_to_response("mesa.html")
