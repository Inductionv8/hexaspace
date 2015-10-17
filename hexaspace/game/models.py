from django.db import models
from django.contrib.auth.models import User

class Jugador(models.Model):
    nombre = models.CharField(default="",max_length=10)
    puntos_victoria = models.IntegerField(default=0)

