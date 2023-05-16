from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateGameForm, JoinGameForm
from .models import Game, GameUser
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.db.models import Count
# Create your views here.


def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO") # TEMPLATE HTML (JINJA) in future


class GameView(ListView):
    model = Game
    template_name = 'exile_app/games.html'
    queryset = Game.objects.annotate(num_players=Count('gameuser'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.queryset
        return context


class GameDetailView(FormMixin, DetailView):
    model = Game
    template_name = 'exile_app/game_detail.html'
    form_class = JoinGameForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        game = self.get_object()
        password = form.cleaned_data.get('password')
        if password == game.password:
            user = self.request.user
            existing_game_user = GameUser.objects.filter(user_id=self.request.user, game_id=game).exists()
            if existing_game_user:
                pass
            else:
                # Add the user to the GameUser table
                GameUser.objects.create(user=self.request.user, game=game)
                messages.success(self.request, 'You have successfully joined the game!')
            return redirect(reverse('exile_app:lobby', kwargs={'game_id': game.id}))
        else:
            messages.error(self.request, 'Incorrect password. Please try again.')
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GameUsersView(ListView):
    model = GameUser
    template_name = 'exile_app/lobby.html'

    def get_queryset(self):
        game = self.kwargs['game_id']
        return GameUser.objects.filter(game_id=game)


class CreateGameView(CreateView):
    model = Game
    template_name = 'exile_app/create_game.html'
    form_class = CreateGameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user=self.request.user, game=game)

        return redirect(reverse('exile_app:lobby', kwargs={'game_id': game.id}))
