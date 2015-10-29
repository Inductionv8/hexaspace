from django.db import models
from django.contrib.auth.models import User, AnonymousUser

class Partida(models.Model):
    num_max_jugadores = models.IntegerField(default=2)
    num_jugadores_actuales = models.IntegerField(default=1)
    creador = models.CharField(default="",max_length=10)
    partida_empezada = models.IntegerField(default=0) # Sera 1 si la partida comenzo.

class Jugador(models.Model):
    #El jugador pertenece a una partida
    partida_id = models.ForeignKey(Partida)
    #El Jugador es un Usuario
    usuario_id = models.OneToOneField(User)
    nombre = models.CharField(default="",max_length=10)
    puntos_victoria = models.IntegerField(default=0)
