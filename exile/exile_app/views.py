from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateGameForm
from .models import Game, GameUser
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
# Create your views here.


def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO") # TEMPLATE HTML (JINJA) in future


class GameView(ListView):
    model = Game
    template_name = 'exile_app/games.html'


class GameDetailView(DetailView):
    model = Game
    template_name = 'exile_app/game_detail.html'


class GameUsersView(ListView):
    model = GameUser
    template_name = 'exile_app/lobby.html'

    def get_queryset(self):
        game = self.kwargs['game_id']
        return GameUser.objects.filter(game_id_id=game)


class CreateGameView(CreateView):
    model = Game
    template_name = 'exile_app/create_game.html'
    form_class = CreateGameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user_id=self.request.user, game_id=game)

        return redirect(reverse('exile_app:lobby', kwargs={'game_id': game.id}))
