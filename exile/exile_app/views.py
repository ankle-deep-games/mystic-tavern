from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView
from .models import Game
# Create your views here.


def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO") # TEMPLATE HTML (JINJA) in future


class GameView(ListView):
    model = Game
    template_name = 'games.html'


