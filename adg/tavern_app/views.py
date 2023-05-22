from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm
from .models import Game, GameUser, Role, Gender
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Count
# Create your views here.

def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO - David Lorenz & Jordan Philyaw - Hackathon May 2023")

def leeroy(request):
    # users are special because they get created with a hashed password with create_user
    # may come back and refactor this to add all 4 in 1 function
    user1 = User.objects.create_user(username='john',email='jlennon@beatles.com',password='imagine')
    user2 = User.objects.create_user(username='paul',email='pmccartney@beatles.com',password='let it be')
    user3 = User.objects.create_user(username='george',email='gharrison@beatles.com',password='my sweet lord')
    user4 = User.objects.create_user(username='ringo',email='rstarr@beatles.com',password='yellow submarine')
    user1.save()
    user2.save()
    user3.save()
    user4.save()

    ## games
    game1 = Game(name="Game Seed 1",creator=user1,password="apple")
    game2 = Game(name="Game Seed 2",creator=user2,password="banana")
    game3 = Game(name="Game Seed 3",creator=user3,password="carrot")
    game4 = Game(name="Game Seed 4",creator=user4,password="date")
    Game.objects.bulk_create([
        game1,
        game2,
        game3,
        game4,
    ])

    ## roles
    role1 = Role(name="WHITEMAGE")
    role2 = Role(name="BLACKMAGE")
    role3 = Role(name="PALADIN")
    role4 = Role(name="ARCHER")
    Role.objects.bulk_create([
        role1,
        role2,
        role3,
        role4,
    ])

    ## genders
    gender1 = Gender(name="MALE")
    gender2 = Gender(name="FEMALE")
    gender3 = Gender(name="NONBINARY")
    Gender.objects.bulk_create([
        gender1,
        gender2,
        gender3,
    ])

    ## gameuser
    gameuser1 = GameUser(
        game=game1,
        user=user1,
        role=role1,
        gender=gender1,
    )
    gameuser2 = GameUser(
        game=game1,
        user=user2,
        role=role2,
        gender=gender2,
    )
    gameuser3 = GameUser(
        game=game1,
        user=user3,
        role=role3,
        gender=gender2,
    )
    gameuser4 = GameUser(
        game=game1,
        user=user4,
        role=role4,
        gender=gender1,
    )
    gameuser5 = GameUser(
        game=game2,
        user=user4,
        role=role2,
        gender=gender1,
    )
    GameUser.objects.bulk_create([
        gameuser1,
        gameuser2,
        gameuser3,
        gameuser4,
        gameuser5,
    ])

    return render(request, 'leeroy.html')

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
        game_id = self.kwargs['game_id']
        return GameUser.objects.filter(game_id=game_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_id = self.kwargs['game_id']
        game = Game.objects.get(id=game_id)
        context['game'] = game

        # Retrieve the creator of the game
        context['creator'] = game.creator
        context['leader'] = GameUser.objects.get(game_id=game_id, user=context['creator'])

        # Check if any player is not ready
        any_player_not_ready = context['object_list'].filter(is_ready=False).exists()
        context['any_player_not_ready'] = any_player_not_ready

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
        kwargs['num_players'] = GameUser.objects.filter(game_id=self.kwargs['game_id']).count()
        return kwargs

    def form_valid(self, form):
        game = Game.objects.get(pk=self.kwargs['game_id'])
        num_players = form.initial['num_players']

        for i in range(1, num_players + 1):
            player_name = form.cleaned_data[f'player_{i}_name']
            player_role = form.cleaned_data[f'player_{i}_role']
            player_gender = form.cleaned_data[f'player_{i}_gender']

            player = GameUser.objects.get(game=game, user__username=player_name)

            player.role = player_role
            player.gender = player_gender
            player.save()

        return super().form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs['game_id']
        return reverse('tavern_app:lobby', kwargs={'game_id': game_id})


class Act1Scene1View(TemplateView):
    template_name = "tavern_app/act1/act1_scene1.html"
