from django.db import models

class Jugador(models.Model):
    nombre = models.CharField(default="",max_length=10)
    puntos_victoria = models.IntegerField(default=0)

