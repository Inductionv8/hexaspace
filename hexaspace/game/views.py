from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.

def homepage(request):
    """
    Si hay algun usuario, lo redirige a la homepage
    """
    user = get_user(request)
    username = user.username
    return render_to_response('main.html',{'username':username})

