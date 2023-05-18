from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm
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
    template_name = 'tavern_app/games.html'
    queryset = Game.objects.annotate(num_players=Count('gameuser'))
    context_object_name = 'games'


class GameDetailView(FormMixin, DetailView):
    model = Game
    template_name = 'tavern_app/game_detail.html'
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
            return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
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
    template_name = 'tavern_app/lobby.html'

    def get_queryset(self):
        game = self.kwargs['game_id']
        return GameUser.objects.filter(game_id=game)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_id = self.kwargs['game_id']
        context['game'] = Game.objects.get(id=game_id)
        return context


class CreateGameView(CreateView):
    model = Game
    template_name = 'tavern_app/create_game.html'
    form_class = CreateGameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user=self.request.user, game=game)

        return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))


class RoleAssignmentView(FormView):
    template_name = 'tavern_app/role_assignment.html'
    form_class = RoleAssignmentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['game_id'] = self.kwargs['game_id']
        return kwargs

    def form_valid(self, form):
        game = Game.objects.get(pk=self.kwargs['game_id'])

        for i in range(1, form.num_players + 1):
            player_name = form.cleaned_data[f'player_{i}_name']
            player_role = form.cleaned_data[f'player_{i}_role']

            player = GameUser.objects.get(game=game, user__username=player_name)

            player.role = player_role
            player.save()

        return super().form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs['game_id']
        return reverse('tavern_app:player_customization', kwargs={'game_id': game_id})


class PlayerCustomizationView(TemplateView):
    template_name = 'tavern_app/player_customization.html'
