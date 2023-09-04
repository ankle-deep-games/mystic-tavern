from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import CreateView, FormView, TemplateView
from .forms import CreateGameForm, JoinGameForm, RoleAssignmentForm, GameDialogueForm, StartGameForm, CombatLogForm
from .models import Game, GameUser, Dialogue, GameDialogue, NPC, Ability, Enemy, GameEnemy, CombatLog, GameLocation, GameTurnOrder
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from .helpers.seed import seed_data
from .helpers.battle import assign_turn_order


def simple_view(request):
    return HttpResponse("LEEEROY JEEEEENKINS! LETS GOOOOOOO - David Lorenz & Jordan Philyaw - Hackathon May 2023")

def seed(request):
    if request.user.is_superuser == False:
        return redirect('tavern_app:home')
    
    seed_data()
    return render(request, 'seed.html')

# /seed/game/:id - faster way to add 3 users to a game when creating games with dobby for manual testing
def add_three_users_to_game(request, game_id):
    if request.user.is_superuser == False:
        return redirect('tavern_app:home')
    
    game = Game(pk=game_id)
    GameUser(game=game,user=User(pk=2)).save()
    GameUser(game=game,user=User(pk=3)).save()
    GameUser(game=game,user=User(pk=4)).save()  
    return HttpResponse("3 users added to game " + str(game_id))

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

class CreateOrJoinView(TemplateView):
    template_name = "tavern_app/home.html"

def games(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see games.', extra_tags="alert alert-danger")
        return redirect('login')
    
    game_list = []
    games = Game.objects.filter(game_over=False).annotate(num_players=Count('gameuser'))

    for game in games:
        is_user_in_game = True if GameUser.objects.filter(game=game, user=request.user) else False
        is_full = True if game.num_players == 4 else False
        is_started = True if game.game_started == True else False
        game_list.append({
            'creator': game.creator,
            'id': game.id,
            'is_full': is_full,
            'is_started': is_started,
            'is_user_in_game': is_user_in_game,
            'name': game.name,
            'num_players': game.num_players,
            })

    context = {
        'game_list': game_list,
    }
    
    return render(request, 'tavern_app/games.html', context)  

def join_game(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to join a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    game_exists = Game.objects.filter(pk=pk).exists()
    if not game_exists:
        messages.error(request, 'Game does not exist.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')
    
    game = Game.objects.get(pk=pk)
    is_user_in_game = True if GameUser.objects.filter(game=game, user=request.user) else False
    if is_user_in_game:
        return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
    
    is_full = True if GameUser.objects.filter(game_id=pk).count() == 4 else False
    if is_full:
        messages.error(request, 'Game is full.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')

    if request.method == 'POST':
        form = JoinGameForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password == game.password:
                if not is_user_in_game:
                    GameUser.objects.create(user=request.user, game=game)
                
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
            else:
                messages.error(request, 'Incorrect password. Please try again.', extra_tags="alert alert-danger")
                return redirect(reverse('tavern_app:join_game', kwargs={'pk': pk}))

        else:
            messages.error(request, 'Something in the form was not valid.', extra_tags="alert alert-danger")

    # else render form
    else:
        form = JoinGameForm()

    context = {
        'form': form,
    }

    return render(request, 'tavern_app/join_game.html', context)

def lobby(request, game_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    if GameUser.objects.filter(user_id=request.user, game_id=game_id).exists() == False:
        messages.error(request, 'Must be in the game to see it.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')
    
    game = Game.objects.get(id=game_id)
    gameusers = GameUser.objects.filter(game_id=game_id)
    is_leader = True if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user else False
    any_player_not_ready = gameusers.filter(is_ready=False).exists()
    num_players_in_lobby = gameusers.count()

    if game.game_started == True:
        gamelocation = GameLocation.objects.get(game=game)
        return redirect(reverse("tavern_app:" + gamelocation.location_type, kwargs={'game_id': game.id, 'act': gamelocation.act, 'number': gamelocation.number}))

    if request.method == 'POST':
        form = StartGameForm(request.POST)
        has_error = False

        if form.is_valid():
            if any_player_not_ready == True:
                messages.error(request, 'All players must be ready to start the game.', extra_tags="alert alert-danger")
                has_error = True

            if game.creator != request.user:
                messages.error(request, 'Game can only be started by party leader.', extra_tags="alert alert-danger")
                has_error = True

            if num_players_in_lobby != 4:
                messages.error(request, 'Game can only be started with 4 players.', extra_tags="alert alert-danger")
                has_error = True

            if has_error:
                return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game_id}))

            # Write first dialogue node for this game, populate game enemies, game_started True
            starting_game_dialogue = GameDialogue(game=game, dialogue=Dialogue.objects.get(pk=1))
            starting_game_dialogue.save()

            # TODO improve later: query all enemies and loop through adding them all into the game
            enemy1 = Enemy.objects.get(pk=1)
            enemy2 = Enemy.objects.get(pk=2)
            gameenemy1 = GameEnemy(
                game=game,
                enemy=enemy1,
                act=1,
                battle=1,
                current_hp=enemy1.start_hp,
                current_mp=enemy1.start_mp,
                current_attack=enemy1.start_attack,
                current_defense=enemy1.start_defense,
                current_myst_attack=enemy1.start_myst_attack,
                current_myst_defense=enemy1.start_myst_defense,
                current_speed=enemy1.start_speed,
            )
            gameenemy2 = GameEnemy(
                game=game,
                enemy=enemy2,
                act=1,
                battle=1,
                current_hp=enemy2.start_hp,
                current_mp=enemy2.start_mp,
                current_attack=enemy2.start_attack,
                current_defense=enemy2.start_defense,
                current_myst_attack=enemy2.start_myst_attack,
                current_myst_defense=enemy2.start_myst_defense,
                current_speed=enemy2.start_speed,
            )
            GameEnemy.objects.bulk_create([
                gameenemy1,
                gameenemy2,
            ])

            game.game_started = True
            game.save()

            gamelocation = GameLocation(game=game, act=1, location_type="scene", number=1)
            gamelocation.save()

            return redirect(reverse("tavern_app:" + gamelocation.location_type, kwargs={'game_id': game.id, 'act': gamelocation.act, 'number': gamelocation.number}))

        else:
            messages.error(request, 'Something in the form was not valid.', extra_tags="alert alert-danger")
            return redirect(reverse('tavern_app:lobby', kwargs={'game_id': game.id}))
            
    else:
        form = StartGameForm(initial={'game_id': game_id})

    context = {
        'game': game,
        'gameusers': gameusers,
        'is_leader': is_leader,
        'any_player_not_ready': any_player_not_ready,
        'num_players_in_lobby': num_players_in_lobby,
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
        attack_ability = Ability.objects.get(pk=1)

        for i in range(1, num_players + 1):
            player_name = form.cleaned_data[f'player_{i}_name']
            player_role = form.cleaned_data[f'player_{i}_role']
            player_gender = form.cleaned_data[f'player_{i}_gender']

            player = GameUser.objects.get(game=game, user__username=player_name)

            player.role = player_role
            player.gender = player_gender

            player.current_hp = player.role.start_hp
            player.current_mp = player.role.start_mp
            player.current_attack = player.role.start_attack
            player.current_defense = player.role.start_defense
            player.current_myst_attack = player.role.start_myst_attack
            player.current_myst_defense = player.role.start_myst_defense
            player.current_speed = player.role.start_speed

            player.ability_1 = attack_ability

            player.save()

        return super().form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs['game_id']
        return reverse('tavern_app:lobby', kwargs={'game_id': game_id})

def scene(request, game_id, act, number):
    scene_num = number
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    if GameUser.objects.filter(user_id=request.user, game_id=game_id).exists() == False:
        messages.error(request, 'Must be in the game to see it.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')
    
    # bool: is current user the party leader
    game = Game.objects.get(pk=game_id)
    is_leader = True if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user else False

    # form submission if game owner clicked next button or dialogue option
    if request.method == 'POST':
        form = GameDialogueForm(request.POST)

        if form.is_valid():
            # get the next dialogue from form values and write to db
            game = Game.objects.get(pk=game_id)
            dialogue = Dialogue.objects.get(pk=form.cleaned_data['dialogue'].id)

            # make sure submission is valid
            latest_game_dialogue_id = GameDialogue.objects.filter(game=game).latest('id').dialogue.id
            gamelocation = GameLocation.objects.get(game=game)
            if dialogue.from_node_id != latest_game_dialogue_id:
                messages.error(request, 'Invalid dialogue choice. Must be connected to previous dialogue.', extra_tags="alert alert-danger")
                return redirect(reverse("tavern_app:" + gamelocation.location_type, kwargs={'game_id': game_id, 'act': act, 'number': scene_num}))
            
            if is_leader == False:
                messages.error(request, 'Only the party leader can progress dialogue.', extra_tags="alert alert-danger")
                return redirect(reverse("tavern_app:" + gamelocation.location_type, kwargs={'game_id': game_id, 'act': act, 'number': scene_num}))

            game_dialogue = GameDialogue(game=game, dialogue=dialogue)
            game_dialogue.save()

        else:
            messages.error(request, 'Something in the dialogue was not valid.', extra_tags="alert alert-danger")

    # else render form
    else:
        form = GameDialogueForm()

    # character_list combines players and npcs into a single list that can later be used to add names and images to dialogues
    character_list = []
    game_users = GameUser.objects.filter(game=game)
    
    # in dialogue we save speakers as "Group Leader" or "Group Member 1"
    # at run time compare those against players in the game so we can display the player username
    for idx, game_user in enumerate(game_users):
        speaker = ""
        if idx == 0:
            speaker = "Group Leader"
        elif idx == 1:
            speaker = "Group Member 1"
        elif idx == 2:
            speaker = "Group Member 2"
        character_list.append({'name': game_user.user.username, 'image': game_user.image(), 'speaker': speaker})

    npcs = NPC.objects.all()
    for npc in npcs:
        character_list.append({'name': npc.name, 'image': npc.image, 'speaker': npc.name})
        
    # game_dialogue_progress_list is the current game's dialogue + names and images
    game_dialogue_progress_list = []
    game_dialogue_progress = GameDialogue.objects.filter(game=game_id)
    for game_dialogue in game_dialogue_progress:
        # only build the list for the current act and scene
        if game_dialogue.dialogue.act == act and game_dialogue.dialogue.scene == scene_num:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == game_dialogue.dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            game_dialogue_progress_list.append({
                'id': game_dialogue.dialogue.pk,
                'node_type': game_dialogue.dialogue.node_type,
                'name': name,
                'text': game_dialogue.dialogue.text,
                'image': image,
                })
        
    # next_dialogue_list queries the game dialogue progress for the next single dialogue or multiple player dialogue choices
    next_dialogue_list = []
    # make sure this act/scene has at least 1 node to prevent errors. filter by act and scene.
    if len(game_dialogue_progress_list) > 0:
        next_dialogue = Dialogue.objects.filter(from_node_id=game_dialogue_progress_list[-1]['id'], act=act, scene=scene_num)
        for dialogue in next_dialogue:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            next_dialogue_list.append({
                'id': dialogue.pk,
                'from_node_id': dialogue.from_node_id,
                'node_type': dialogue.node_type,
                'name': name,
                'text': dialogue.text,
                'image': image,
                })
        
    # TODO https://trello.com/c/oL6acc6m/127-end-of-act-1-scene-1-final-button-goes-to-battle

    context = {
        'game_id': game_id,
        'game_dialogue_progress_list': game_dialogue_progress_list,
        'next_dialogue_list': next_dialogue_list,
        'form': form,
        'is_leader': is_leader,
    }

    return render(request, 'tavern_app/scene.html', context)

def battle(request, game_id, act, number):
    battle_num = number
    if not request.user.is_authenticated:
        messages.error(request, 'Must be logged in to see a game.', extra_tags="alert alert-danger")
        return redirect('login')
    
    if GameUser.objects.filter(user_id=request.user, game_id=game_id).exists() == False:
        messages.error(request, 'Must be in the game to see it.', extra_tags="alert alert-danger")
        return redirect('tavern_app:games')

    game = Game.objects.get(pk=game_id)
    player = GameUser.objects.get(game_id=game_id, user=request.user)

    if request.method == 'POST':
        form = CombatLogForm(request.POST)

        if form.is_valid():
            # TODO adjust to handle AOE abilities where mulitiple enemies are hit
            enemy = GameEnemy.objects.get(game_id=game_id, enemy=Enemy(form.cleaned_data['enemy'].id))
            ability = Ability.objects.get(pk=form.cleaned_data['ability'].id)

            unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
            if unit_turn.gameuser:
                is_request_user_turn = True if unit_turn.gameuser.user == request.user else False
            else:
                is_request_user_turn = False
            
            if is_request_user_turn:
                messages.success(request, 'Yes! It was that users turn to attack', extra_tags="alert alert-success")

                combat_log = CombatLog(
                    game = game,
                    player = player.user,
                    enemy = enemy.enemy,
                    player_or_enemy_took_action = "player",
                    ability = ability,
                    damage = ability.max_damage, # for testing do the max damage. will update later
                    unit_previous_hp = enemy.current_hp,
                    unit_resulting_hp = enemy.current_hp - ability.max_damage,
                    ability_mp_cost = ability.mp_cost,
                    unit_previous_mp = player.current_mp,
                    unit_resulting_mp = player.current_mp - ability.mp_cost,
                    ability_min_damage = ability.min_damage,
                    ability_max_damage = ability.max_damage,
                    )
                combat_log.save()

                enemy.current_hp = enemy.current_hp - ability.max_damage
                enemy.save()

                player.current_mp = player.current_mp - ability.mp_cost
                player.save()

                unit_turn.is_their_turn = False
                unit_turn.save()
            else:
                messages.error(request, 'IT IS NOT YOUR TURN TO ATTACK!', extra_tags="alert alert-danger")

            # TODO update redirect to current battle
            return redirect(reverse("tavern_app:battle", kwargs={'game_id': game.id, 'act': 1, 'number': 1}))

    # else render form
    else:
        form = CombatLogForm()

    gameusers = GameUser.objects.filter(game_id=game_id)
    gameenemies = GameEnemy.objects.filter(game_id=game_id, act=act, battle=battle_num)

    assign_turn_order(game=game, gameusers=gameusers, gameenemies=gameenemies)

    unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)

    # TODO clean up after working
    if unit_turn.gameenemy:
        attacking_enemy = unit_turn
        print("enemy turn is:")
        print(attacking_enemy)

        ## start by only using regular attack - later choose one of their abilities to cast
        attacking_enemy_ability = attacking_enemy.gameenemy.enemy.ability_1
        print("attacking enemy attack:")
        print(attacking_enemy_ability)

        ## start by attacking first player in loop - then select an alive player to attack at random
        attacking_enemey_target_player = '' # TODO instantiate this as an empty <class 'tavern_app.models.GameUser'>
        for gameuser in gameusers:
            attacking_enemey_target_player = gameuser
        print("target player is")
        print(attacking_enemey_target_player)

        ## do damage to that player and update combat log
        combat_log = CombatLog(
            game = game,
            player = attacking_enemey_target_player.user,
            enemy = attacking_enemy.gameenemy.enemy,
            player_or_enemy_took_action = "enemy",
            ability = attacking_enemy_ability,
            damage = attacking_enemy_ability.max_damage, # for testing do the max damage. will update later
            unit_previous_hp = attacking_enemey_target_player.current_hp,
            unit_resulting_hp = attacking_enemey_target_player.current_hp - attacking_enemy_ability.max_damage,
            ability_mp_cost = attacking_enemy_ability.mp_cost,
            unit_previous_mp = attacking_enemy.gameenemy.current_mp,
            unit_resulting_mp = attacking_enemy.gameenemy.current_mp - attacking_enemy_ability.mp_cost,
            ability_min_damage = attacking_enemy_ability.min_damage,
            ability_max_damage = attacking_enemy_ability.max_damage,
            )
        combat_log.save()

        attacking_enemey_target_player.current_hp = attacking_enemey_target_player.current_hp - attacking_enemy_ability.max_damage
        attacking_enemey_target_player.save()

        attacking_enemy.gameenemy.current_mp = attacking_enemy.gameenemy.current_mp - attacking_enemy_ability.mp_cost
        attacking_enemy.save()

        unit_turn.is_their_turn = False
        unit_turn.save()

        messages.info(request, f'{attacking_enemy.gameenemy.enemy.name} attacked {attacking_enemey_target_player.user.username} for {attacking_enemy_ability.max_damage} as well', extra_tags="alert alert-info")

        ## split out the assign turn order function and rerun it to assign a new turn order.
        assign_turn_order(game=game, gameusers=gameusers, gameenemies=gameenemies)

        ## if next enemy one to attack in an enemy do it again


    combat_log_debug = CombatLog.objects.filter(game=game)
    print("***COMBAT LOG***")
    for log in combat_log_debug:
        print(log)
    print("***COMBAT LOG***\n")

    game_turn_order = GameTurnOrder.objects.filter(game=game)
    print("***TURN ORDER***")
    for turn_order in game_turn_order:
        print(turn_order)
        if turn_order.is_their_turn:
            print("-----^ their turn ^-----")
    print("***TURN ORDER***")

    ## TODO reassign unit_turn for debugging on frontend
    unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
    if unit_turn.gameuser:
        is_request_user_turn = True if unit_turn.gameuser.user == request.user else False
    else:
        is_request_user_turn = False

    context = {
        'game_id': game_id,
        'gameusers': gameusers,
        'gameenemies': gameenemies,
        'form': form,
        'player': player,
        'unit_turn': unit_turn,
        'is_request_user_turn': is_request_user_turn,
    }

    return render(request, 'tavern_app/battle.html', context)
