from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm, GameDialogueForm, StartGameForm
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
    game1 = Game(name="Game Seed 1",creator=user1, game_started=False, game_over=False, password="apple")
    game2 = Game(name="Game Seed 2",creator=user2, game_started=False, game_over=False, password="banana")
    game3 = Game(name="Game Seed 3",creator=user3, game_started=False, game_over=False, password="carrot")
    game4 = Game(name="Game Seed 4",creator=user4, game_started=False, game_over=False, password="date")
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
    # TODO fill out all act 1 scene 1 dialogue https://trello.com/c/ynY1d4dX/104-act-1-scene-1-bar-scene-flowchart
    node1 = Dialogue(from_node_id=0, node_type="narration", speaker="narrator", text="Your group finds themselves teleported to an abandoned alleyway in what looks like a quaint old village. The narrow passage is dimly lit, and the silence is broken by the distant sounds of chatter and laughter. Suddenly, two drunk men spot your group and stagger towards you, their eyes gleaming with mischief.")
    node2 = Dialogue(from_node_id=1, node_type="talk", speaker="drunk old man", text="You there! I have a quest for you.")
    # save nodes 1 at a time so they are assigned the correct id
    node1.save()
    node2.save()

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

def lobby(request, game_id):
    game = Game.objects.get(id=game_id)
    gameusers = GameUser.objects.filter(game_id=game_id)
    leader = GameUser.objects.get(game_id=game_id, user=game.creator)
    any_player_not_ready = gameusers.filter(is_ready=False).exists()

    if game.game_started == True:
        return redirect(reverse('tavern_app:act1_scene1', kwargs={'game_id': game.id}))

    if request.method == 'POST':
        form = StartGameForm(request.POST)
        
        if form.is_valid():
            # TODO add better error messaging for any players not ready https://trello.com/c/tkGuaIp0/114-add-validation-to-all-forms-views
            if any_player_not_ready == True:
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))

            # TODO add better error messaging for not started by creator https://trello.com/c/tkGuaIp0/114-add-validation-to-all-forms-views
            if game.creator != request.user:
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))

            # TODO add better error messaging if game wasn't started from lobby with same game_id in url https://trello.com/c/tkGuaIp0/114-add-validation-to-all-forms-views
            if form.cleaned_data['game_id'] != game.pk:
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))

            # Write first dialogue node for this game and game_started True
            starting_game_dialogue = GameDialogue(game=game, dialogue=Dialogue.objects.get(pk=1))
            starting_game_dialogue.save()
            game.game_started = True
            game.save()

            return redirect(reverse('tavern_app:act1_scene1', kwargs={'game_id': game.id}))

        else:
            # TODO better handling of if form is not valid https://trello.com/c/tkGuaIp0/114-add-validation-to-all-forms-views
            return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
            
    else:
        form = StartGameForm(initial={'game_id': game_id})

    context = {
        'game': game,
        'gameusers': gameusers,
        'leader': leader,
        'any_player_not_ready': any_player_not_ready,
        'form': form,
    }
    
    return render(request, 'tavern_app/lobby.html', context)    

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

# TODO
# 1. https://trello.com/c/Ms7zgd3S/108-refactor-story-views-and-forms-to-classed-based-views
# 2. https://trello.com/c/nXMi0HR5/109-story-url-routing
# 3. https://trello.com/c/4tBieF3j/110-only-allow-game-owner-to-submit-dialogue-choices-but-show-it-to-others
def act1_scene1_view(request, game_id):

    # form submission if game owner clicked a dialogue option
    if request.method == 'POST':
        form = GameDialogueForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            # save selected choice
            form.save()
            # get the next dialogue option from non player character and write to db
            nextGame = Game.objects.get(pk=game_id)
            nextDialogue = Dialogue.objects.get(from_node_id=form.cleaned_data["dialogue"].id)
            nextGameDialogue = GameDialogue(game=nextGame, dialogue=nextDialogue)
            nextGameDialogue.save()

    # else render form
    else:
        form = GameDialogueForm()

    context = {
        'game_id': game_id,
        'dialogues': Dialogue.objects.all(),
        'dialogue_progress': GameDialogue.objects.filter(game=game_id),
        'dialogue_latest': GameDialogue.objects.filter(game=game_id).latest('id').id,
        'form': form
    }
    return render(request, 'tavern_app/act1/act1_scene1.html', context)
