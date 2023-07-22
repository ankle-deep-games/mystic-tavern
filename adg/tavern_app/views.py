from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm
from .models import Game, GameUser, Role, Gender, Dialogue, GameDialogue
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Count
from django.http import JsonResponse
# Create your views here.

def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO - David Lorenz & Jordan Philyaw - Hackathon May 2023")

def leeroy(request):
    # users are special because they get created with a hashed password with create_user
    user1 = User.objects.create_user(username='john',email='jlennon@beatles.com',password='imagine')
    user2 = User.objects.create_user(username='paul',email='pmccartney@beatles.com',password='let it be')
    user3 = User.objects.create_user(username='george',email='gharrison@beatles.com',password='my sweet lord')
    user4 = User.objects.create_user(username='ringo',email='rstarr@beatles.com',password='yellow submarine')
    user5 = User.objects.create_user(username='eleanor',email='erigby@beatles.com',password='lonely people')
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user5.save()

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
    role1 = Role(name="WHITEMAGE", start_hp=100, start_attack=10, start_defense=20, start_myst_attack=15, start_myst_defense=20, start_speed=25)
    role2 = Role(name="BLACKMAGE", start_hp=80, start_attack=15, start_defense=10, start_myst_attack=35, start_myst_defense=10, start_speed=30)
    role3 = Role(name="PALADIN", start_hp=120, start_attack=20, start_defense=30, start_myst_attack=10, start_myst_defense=20, start_speed=20)
    role4 = Role(name="ARCHER", start_hp=85, start_attack=35, start_defense=15, start_myst_attack=10, start_myst_defense=10, start_speed=30)
    role5 = Role(name="BARD", start_hp=90, start_attack=20, start_defense=20, start_myst_attack=20, start_myst_defense=20, start_speed=20)
    Role.objects.bulk_create([
        role1,
        role2,
        role3,
        role4,
        role5,
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
        is_ready=True,
    )
    gameuser2 = GameUser(
        game=game1,
        user=user2,
        role=role2,
        gender=gender2,
        is_ready=True,
    )
    gameuser3 = GameUser(
        game=game1,
        user=user3,
        role=role3,
        gender=gender2,
        is_ready=True,
    )
    gameuser4 = GameUser(
        game=game1,
        user=user4,
        role=role4,
        gender=gender1,
        is_ready=True,
    )
    gameuser5 = GameUser(
        game=game1,
        user=user5,
        role=role5,
        gender=gender2,
        is_ready=True,
    )
    gameuser6 = GameUser(
        game=game2,
        user=user2,
        role=role2,
        gender=gender1,
        is_ready=True,
    )
    GameUser.objects.bulk_create([
        gameuser1,
        gameuser2,
        gameuser3,
        gameuser4,
        gameuser5,
        gameuser6,
    ])

    ## dialogue
    node1 = Dialogue(from_node_id=0, node_type="narration", speaker="narrator", text="Welcome to the enchanting world of mystic tavern. You stumble into the tavern and see a strange drunk old man.")
    node2 = Dialogue(from_node_id=1, node_type="talk", speaker="drunk old man", text="You there! I have a quest for you.")
    node3 = Dialogue(from_node_id=2, node_type="player_response", speaker="party leader", text="A quest?! I accept.")
    node4 = Dialogue(from_node_id=2, node_type="player_response", speaker="party leader", text="What's in it for me?")
    node5 = Dialogue(from_node_id=2, node_type="player_response", speaker="party leader", text="Hard pass.")
    node6 = Dialogue(from_node_id=3, node_type="talk", speaker="drunk old man", text="Praise Be you have accepted my quest. You must defend our land from The Creature.")
    node7 = Dialogue(from_node_id=4, node_type="talk", speaker="drunk old man", text="In it for you? Why, the satisfaction of a job well done.. Hic!")
    node8 = Dialogue(from_node_id=5, node_type="talk", speaker="drunk old man", text="How dissapointing to hear you will not accept my quest.")
    # save nodes 1 at a time so they are assigned the correct id
    node1.save()
    node2.save()
    node3.save()
    node4.save()
    node5.save()
    node6.save()
    node7.save()
    node8.save()

    # only temporarily seeding gamedialogue for game 1 until we hook up the START GAME button to update DB
    # idea is that game start button will write to GameDialogue
    gameDialogue1 = GameDialogue(game=game1, dialogue=node1)
    gameDialogue2 = GameDialogue(game=game1, dialogue=node2)
    # to test we can filter by game
    gameDialogue3 = GameDialogue(game=game2, dialogue=node8)
    gameDialogue1.save()
    gameDialogue2.save()
    gameDialogue3.save()

    return render(request, 'leeroy.html')

def live_update_prototype(request):
    games = Game.objects.all()
    return JsonResponse({"games":list(games.values())})

def live_update_prototype_view(request):
    context = {
        'games': Game.objects.all()
    }
    return render(request, 'liveupdateprototype.html', context)

def live_update_prototype_redirect_view(request):
    context = {
        'gameCount': Game.objects.all().count()
    }
    return render(request, 'liveupdateprototyperedirect.html', context)

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

# TODO - so much to do to make cleaner - this is rough proof of concept
def act1_scene1_view(request, game_id):
    context = {
        'game_id': game_id,
        'dialogues': Dialogue.objects.all(),
        'dialogue_progress': GameDialogue.objects.filter(game=game_id),
        'dialogue_latest': GameDialogue.objects.filter(game=game_id).latest('id').id
    }
    return render(request, 'tavern_app/act1/act1_scene1.html', context)
