from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, reverse, get_object_or_404
from django.shortcuts import render
from django.views.generic import CreateView

from .constants import QUEST_1_NODE, QUEST_2_NODE, QUEST_3_NODE, END_OF_SCENE_1_NODES, \
    NIGHT_DECISION_ALL_REST_NODE, NIGHT_DECISION_ROTATE_REST_NODE, NIGHT_DECISION_PLAYER_1_WATCH_NODE, \
    NIGHT_DECISION_PLAYER_2_WATCH_NODE, NIGHT_DECISION_PLAYER_3_WATCH_NODE, NIGHT_DECISION_PLAYER_4_WATCH_NODE, \
    PLAYER_1_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE, PLAYER_2_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE, \
    PLAYER_3_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE, PLAYER_4_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE, \
    PLAYER_1_WEAPON_UPGRADE_NODE, PLAYER_2_WEAPON_UPGRADE_NODE, PLAYER_3_WEAPON_UPGRADE_NODE, \
    PLAYER_4_WEAPON_UPGRADE_NODE, ACT_1_SCENE_1_ENDING_NODE, ACT_1_SCENE_2_STARTING_NODE, \
    ACT_1_SCENE_2_ENDING_NODE_CHOICE_1, ACT_1_SCENE_2_ENDING_NODE_CHOICE_2, ACT_1_SCENE_3_STARTING_NODE, \
    ACT_1_SCENE_4_STARTING_NODE, ACT_1_SCENE_2_ENDING_NODE_CHOICE_3, ACT_1_SCENE_5_STARTING_NODE, \
    ACT_1_SCENE_6_STARTING_NODE, ACT_1_SCENE_3_ENDING_NODE, ACT_1_SCENE_4_ENDING_NODE, ACT_1_SCENE_5_ENDING_NODE
from .forms import (
    CreateGameForm,
    JoinGameForm,
    RoleAssignmentForm,
    GameDialogueForm,
    StartGameForm,
    CombatLogForm, BaseRoleAssignmentFormSet,
)
from .helpers.battle import (
    gameuser_attack_single_gameenemy_and_save,
    gameuser_heal_single_gameuser_and_save,
    calc_is_request_user_turn,
    gameuser_buff_single_gameuser_and_save,
    calc_turns_and_execute_enemy_turns, check_and_handle_battle_over, init_gameusers_current_battle_starting_stats,
)
from .helpers.choice import quest_choice_1, quest_choice_2_and_3, night_choice_all_rest, night_choice_rotate_watch, \
    night_choice_one_player_watch
from .helpers.game_lifecycle import init_game_enemies, role_assignment_init_player_stats, \
    equip_player_with_starting_weapon1_armor1_ability2, player_weapon2_upgrade
from .helpers.redirect import check_redirect_criteria
from .helpers.scene import (
    get_character_list,
    get_game_dialogue_progress_list,
    get_next_dialogue_list, check_and_regex_replace_dialogue,
)
from .helpers.seed import seed_data
from .models import (
    Game,
    GameUser,
    Dialogue,
    GameDialogue,
    Ability,
    GameEnemy,
    CombatLog,
    GameLocation,
    GameTurnOrder,
    SceneImage,
)


def homepage(request):
    criteria = [
        {
            "condition": request.user.is_authenticated,
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    return render(request, 'tavern_app/home.html')


def seed(request):
    criteria = [
        {
            "condition": not request.user.is_superuser,
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    seed_data()
    return render(request, "tavern_app/seed.html")


# /seed/game/:id - faster way to add 3 users to a game when creating games with dobby for manual testing
def add_three_users_to_game(request, game_id):
    criteria = [
        {
            "condition": not request.user.is_superuser,
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    game = Game(pk=game_id)
    GameUser(game=game, user=User(pk=2)).save()
    GameUser(game=game, user=User(pk=3)).save()
    GameUser(game=game, user=User(pk=4)).save()
    return HttpResponse("3 users added to game " + str(game_id))


def games(request):
    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "error",
            "message": "Must be logged in to see games. Log in or click the link below to register a new account.",
            "redirect_url": "login",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    game_list = []
    games_queryset = Game.objects.filter(game_over=False).annotate(num_players=Count("gameuser"))

    for game in games_queryset:
        game_list.append(
            {
                "creator": game.creator,
                "id": game.id,
                "is_full": game.num_players == 4,
                "is_started": game.game_started,
                "is_user_in_game": GameUser.objects.filter(game=game, user=request.user).exists(),
                "name": game.name,
                "num_players": game.num_players,
            }
        )

    context = {
        "game_list": game_list,
    }

    return render(request, "tavern_app/games.html", context)


def join_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to join a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{pk}",
        },
        {
            "condition": is_user_in_game,
            "use_reverse": True,
            "redirect_url": "tavern_app:lobby",
            "kwargs": {"game_id": game.id},
        },
        {
            "condition": GameUser.objects.filter(game_id=pk).count() == 4,
            "message_type": "error",
            "message": "Game is full.",
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        form = JoinGameForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            if password == game.password:
                if not is_user_in_game:
                    GameUser.objects.create(user=request.user, game=game)

                return redirect(
                    reverse("tavern_app:lobby", kwargs={"game_id": game.id})
                )
            else:
                messages.error(
                    request,
                    "Incorrect password. Please try again.",
                    extra_tags="alert alert-danger",
                )
                return redirect(reverse("tavern_app:join_game", kwargs={"pk": pk}))

        else:
            messages.error(
                request,
                "Something in the form was not valid.",
                extra_tags="alert alert-danger",
            )
    else:
        form = JoinGameForm()

    context = {
        "form": form,
    }

    return render(request, "tavern_app/join_game.html", context)


def lobby(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    if game.game_started:
        gamelocation = GameLocation.objects.get(game=game)
    else:
        gamelocation = GameLocation()

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "use_reverse": True,
            "redirect_url": "tavern_app:join_game",
            "kwargs": {"pk": game_id}
        },
        {
            "condition": game.game_over,
            "use_reverse": True,
            "redirect_url": "tavern_app:gameover",
            "kwargs": {"game_id": game_id}
        },
        {
            "condition": game.game_started,
            "use_reverse": True,
            "redirect_url": "tavern_app:" + gamelocation.location_type,
            "kwargs": {
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            }
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    gameusers = GameUser.objects.filter(game_id=game_id)
    any_player_not_ready = gameusers.filter(is_ready=False).exists()
    num_players_in_lobby = gameusers.count()

    if request.method == "POST":
        form = StartGameForm(request.POST)
        has_error = False

        if form.is_valid():
            if any_player_not_ready:
                messages.error(
                    request,
                    "All players must be ready to start the game.",
                    extra_tags="alert alert-danger",
                )
                has_error = True

            if game.creator != request.user:
                messages.error(
                    request,
                    "Game can only be started by party leader.",
                    extra_tags="alert alert-danger",
                )
                has_error = True

            if num_players_in_lobby != 4:
                messages.error(
                    request,
                    "Game can only be started with 4 players.",
                    extra_tags="alert alert-danger",
                )
                has_error = True

            if has_error:
                return redirect(
                    reverse("tavern_app:lobby", kwargs={"game_id": game_id})
                )

            # Write first dialogue node for this game, populate game enemies, game_started True
            starting_game_dialogue = GameDialogue(
                game=game, dialogue=Dialogue.objects.get(pk=1)
            )
            starting_game_dialogue.save()

            init_game_enemies(game=game)

            gamelocation = GameLocation(
                game=game, act=1, location_type="scene", number=1
            )
            gamelocation.save()

            game.game_started = True
            game.save()

            return redirect(
                reverse(
                    "tavern_app:" + gamelocation.location_type,
                    kwargs={
                        "game_id": game.id,
                        "act": gamelocation.act,
                        "number": gamelocation.number,
                    },
                )
            )

        else:
            messages.error(
                request,
                "Something in the form was not valid.",
                extra_tags="alert alert-danger",
            )
            return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))

    else:
        form = StartGameForm(initial={"game_id": game_id})

    context = {
        "game_id": game_id,
        "game": game,
        "gameusers": gameusers,
        "is_leader": request.user == GameUser.objects.get(game=game, user=game.creator).user,
        "any_player_not_ready": any_player_not_ready,
        "num_players_in_lobby": num_players_in_lobby,
        "form": form,
    }

    return render(request, "tavern_app/lobby.html", context)


def lobby_get_updates(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    new_url = ""
    if game.game_started:
        gamelocation = GameLocation.objects.get(game=game)
        new_url = reverse(
            "tavern_app:" + gamelocation.location_type,
            kwargs={
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            },
        )
    if game.game_over:
        new_url = reverse("tavern_app:gameover", kwargs={"game_id": game_id})

    gameusers = GameUser.objects.filter(game=game)
    gameusers_json = list(
        gameusers.values(
            "id", "user__username", "gender__name", "role__name", "role__display_name", "role__start_hp",
            "role__start_mp",
            "role__start_attack",
            "role__start_defense", "role__start_myst_attack", "role__start_myst_defense", "role__start_speed"
        )
    )

    data = {
        "gameusers": gameusers_json,
        "new_url": new_url,
    }
    return JsonResponse(data)


class CreateGameView(CreateView):
    model = Game
    template_name = "tavern_app/create_game.html"
    form_class = CreateGameForm

    def get(self, request, *args, **kwargs):
        criteria = [
            {
                "condition": not request.user.is_authenticated,
                "message_type": "error",
                "message": "Must be logged in to create games. Log in or click the link below to register a new "
                           "account.",
                "redirect_url": "login",
            },
        ]
        redirect_response = check_redirect_criteria(request, criteria)
        if redirect_response:
            return redirect_response

        # If criteria check passes, proceed with normal behavior
        return super(CreateGameView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user=self.request.user, game=game)

        return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))


def role_assignment(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    if game.game_started:
        gamelocation = GameLocation.objects.get(game=game)
    else:
        gamelocation = GameLocation()
    is_leader = request.user == GameUser.objects.get(game=game, user=game.creator).user

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
        {
            "condition": game.game_over,
            "use_reverse": True,
            "redirect_url": "tavern_app:gameover",
            "kwargs": {"game_id": game_id}
        },
        {
            "condition": game.game_started,
            "use_reverse": True,
            "redirect_url": "tavern_app:" + gamelocation.location_type,
            "kwargs": {
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            }
        },
        {
            "condition": not is_leader,
            "message": "Only party leader can assign roles.",
            "message_type": "error",
            "use_reverse": True,
            "redirect_url": "tavern_app:lobby",
            "kwargs": {"game_id": game.id}
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    gameusers_queryset = GameUser.objects.filter(game=game)
    print("GAMEUSERS QUERYSET")
    print(gameusers_queryset)

    role_assignment_form_set = inlineformset_factory(
        parent_model=Game,
        model=GameUser,
        form=RoleAssignmentForm,
        formset=BaseRoleAssignmentFormSet,
        extra=0,
        max_num=4,  # Maximum number of forms
        can_delete=False,
    )

    if request.method == 'POST':
        print("INSIDE THE POST")
        print(request.POST)
        formset = role_assignment_form_set(request.POST, instance=game, queryset=gameusers_queryset)
        if formset.is_valid():
            role_assignment_init_player_stats(formset)
            formset.save()  # Save the formset data after updating the players
            return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))
    else:
        formset = role_assignment_form_set(instance=game, queryset=gameusers_queryset)

    return render(request, 'tavern_app/role_assignment.html', {'formset': formset})


def scene(request, game_id, act, number):
    scene_num = number
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    gamelocation = get_object_or_404(GameLocation, game=game)
    is_leader = request.user == GameUser.objects.get(game=game, user=game.creator).user

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
        {
            "condition": game.game_over,
            "use_reverse": True,
            "redirect_url": "tavern_app:gameover",
            "kwargs": {"game_id": game_id},
        },
        {
            "condition": gamelocation.act != act or gamelocation.number != scene_num or gamelocation.location_type != "scene",
            "use_reverse": True,
            "redirect_url": "tavern_app:" + gamelocation.location_type,
            "kwargs": {
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            }
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    # form submission if game owner clicked next button or dialogue option
    if request.method == "POST":
        form = GameDialogueForm(request.POST)

        if form.is_valid():
            # get the next dialogue from form values and write to db
            game = Game.objects.get(pk=game_id)
            dialogue = Dialogue.objects.get(pk=form.cleaned_data["dialogue"].id)

            # make sure submission is valid
            latest_game_dialogue_id = (
                GameDialogue.objects.filter(game=game).latest("id").dialogue.id
            )
            has_error = False
            error_msg = ""
            new_url = ""
            if dialogue.from_node_id != latest_game_dialogue_id:
                has_error = True
                error_msg = (
                    "Invalid dialogue choice. Must be connected to previous dialogue."
                )

            if not is_leader:
                has_error = True
                error_msg = "Only the party leader can progress dialogue."

            if not has_error:
                game_dialogue = GameDialogue(game=game, dialogue=dialogue)
                replaced_text = check_and_regex_replace_dialogue(game=game, dialogue=dialogue)
                # only populate regex text if there was a regex replace
                if dialogue.text != replaced_text:
                    game_dialogue.regex_replaced_text_or_empty = replaced_text
                game_dialogue.save()

                #########
                # Act 1 #
                #########
                if act == 1:
                    ###########
                    # SCENE 1 #
                    ###########
                    if scene_num == 1 and dialogue.id == ACT_1_SCENE_1_ENDING_NODE:
                        # write next game dialogue first node of act 1, scene 2
                        next_scene_dialogue = GameDialogue(
                            game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_2_STARTING_NODE)
                        )
                        next_scene_dialogue.save()

                        # update gamelocation to act 1, scene 2
                        gamelocation.location_type = "scene"
                        gamelocation.number = 2
                        gamelocation.save()

                        # create new_url so front end can redirect player
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                    ###########
                    # SCENE 2 #
                    ###########
                    if scene_num == 2 and dialogue.id == ACT_1_SCENE_2_ENDING_NODE_CHOICE_1:
                        # write next game dialogue first node of act 1, scene 3
                        next_scene_dialogue = GameDialogue(
                            game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_3_STARTING_NODE)
                        )
                        next_scene_dialogue.save()

                        # update gamelocation to act 1, scene 3
                        gamelocation.location_type = "scene"
                        gamelocation.number = 3
                        gamelocation.save()

                        # create new_url so front end can redirect player
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                    if scene_num == 2 and dialogue.id == ACT_1_SCENE_2_ENDING_NODE_CHOICE_2:
                        # write next game dialogue first node of act 1, scene 4
                        next_scene_dialogue = GameDialogue(
                            game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_4_STARTING_NODE)
                        )
                        next_scene_dialogue.save()

                        # update gamelocation to act 1, scene 4
                        gamelocation.location_type = "scene"
                        gamelocation.number = 4
                        gamelocation.save()

                        # create new_url so front end can redirect player
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                    if scene_num == 2 and dialogue.id == ACT_1_SCENE_2_ENDING_NODE_CHOICE_3:
                        # write next game dialogue first node of act 1, scene 5
                        next_scene_dialogue = GameDialogue(
                            game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_5_STARTING_NODE)
                        )
                        next_scene_dialogue.save()

                        # update gamelocation to act 1, scene 5
                        gamelocation.location_type = "scene"
                        gamelocation.number = 5
                        gamelocation.save()

                        # create new_url so front end can redirect player
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                    ###########
                    # SCENE 3 #
                    ###########
                    if scene_num == 3 and dialogue.id == ACT_1_SCENE_3_ENDING_NODE:
                        # write next game dialogue first node of act 1, scene 6
                        # TODO hook these up right.
                        # TODO its going from scene 3 to scene 6 but with no scene image or dialogue display
                        # Instead of getting and inserting a node. I need to create my own node
                        # Node is 100
                        # from_node is 35, 38, 41
                        # TODO https://trello.com/c/N6oIJUrp/323-scene-3-to-6
                        # TODO Change GameDialogue
                        # TODO dialogue = models.OneToOneField(Dialogue, on_delete=models.PROTECT, null=True)
                        # Removes the foreign key requirement so I can commit a Dialogue() that doesn't exist in DB
                        # FK requires it exist in DB. This new way it's an optional join and we can write an in memory
                        # version of Dialogue() and save it directly.
                        node100 = Dialogue(from_node_id=ACT_1_SCENE_3_ENDING_NODE, node_type="narration", speaker="Narrator",
                                           text="They open the door to the tavern to leave and sense an unusual "
                                                "change in the air. Something inside them feels different—strength, "
                                                "confidence, or something else they can't quite grasp.",
                                           act=1, scene=ACT_1_SCENE_6_STARTING_NODE)

                        next_scene_dialogue = GameDialogue(
                            game=game, dialogue=node100
                        )
                        next_scene_dialogue.save()

                        # update gamelocation to act 1, scene 6
                        gamelocation.location_type = "scene"
                        gamelocation.number = 6
                        gamelocation.save()

                        # create new_url so front end can redirect player
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                        ###########
                        # SCENE 4 #
                        ###########
                        if scene_num == 4 and dialogue.id == ACT_1_SCENE_4_ENDING_NODE:
                            # write next game dialogue first node of act 1, scene 6
                            next_scene_dialogue = GameDialogue(
                                game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_6_STARTING_NODE)
                            )
                            next_scene_dialogue.save()

                            # update gamelocation to act 1, scene 6
                            gamelocation.location_type = "scene"
                            gamelocation.number = 6
                            gamelocation.save()

                            # create new_url so front end can redirect player
                            new_url = reverse(
                                "tavern_app:" + gamelocation.location_type,
                                kwargs={
                                    "game_id": game.id,
                                    "act": gamelocation.act,
                                    "number": gamelocation.number,
                                },
                            )

                        ###########
                        # SCENE 5 #
                        ###########
                        if scene_num == 5 and dialogue.id == ACT_1_SCENE_5_ENDING_NODE:
                            # write next game dialogue first node of act 1, scene 6
                            next_scene_dialogue = GameDialogue(
                                game=game, dialogue=Dialogue.objects.get(pk=ACT_1_SCENE_6_STARTING_NODE)
                            )
                            next_scene_dialogue.save()

                            # update gamelocation to act 1, scene 6
                            gamelocation.location_type = "scene"
                            gamelocation.number = 6
                            gamelocation.save()

                            # create new_url so front end can redirect player
                            new_url = reverse(
                                "tavern_app:" + gamelocation.location_type,
                                kwargs={
                                    "game_id": game.id,
                                    "act": gamelocation.act,
                                    "number": gamelocation.number,
                                },
                            )

                    # TODO https://trello.com/c/jYRmW3vN/309-weapon1-armor1-ability2-real-nodes
                    if scene_num == 1 and dialogue.id == PLAYER_1_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE:
                        equip_player_with_starting_weapon1_armor1_ability2(game=game, player_num=1)
                    elif scene_num == 1 and dialogue.id == PLAYER_2_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE:
                        equip_player_with_starting_weapon1_armor1_ability2(game=game, player_num=2)
                    elif scene_num == 1 and dialogue.id == PLAYER_3_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE:
                        equip_player_with_starting_weapon1_armor1_ability2(game=game, player_num=3)
                    elif scene_num == 1 and dialogue.id == PLAYER_4_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE:
                        equip_player_with_starting_weapon1_armor1_ability2(game=game, player_num=4)

                    # TODO https://trello.com/c/cS7s3OEs/217-combat-update-gamelocation-when-winning-and-losing-battles-depending-on-next-step-in-game
                    if scene_num == 1 and dialogue.id in END_OF_SCENE_1_NODES:
                        # TODO update real nodes. no longer end of scene 1
                        gamelocation.location_type = "battle"
                        gamelocation.save()
                        new_url = reverse(
                            "tavern_app:" + gamelocation.location_type,
                            kwargs={
                                "game_id": game.id,
                                "act": gamelocation.act,
                                "number": gamelocation.number,
                            },
                        )

                #########
                # Act 2 #
                #########
                if act == 1:  # TODO change back to act 1
                    # TODO https://trello.com/c/FOmJYpJ3/310-assign-real-weapon-upgrade-nodes
                    if scene_num == 1 and dialogue.id == PLAYER_1_WEAPON_UPGRADE_NODE:
                        player_weapon2_upgrade(game=game, player_num=1)
                    elif scene_num == 1 and dialogue.id == PLAYER_2_WEAPON_UPGRADE_NODE:
                        player_weapon2_upgrade(game=game, player_num=2)
                    elif scene_num == 1 and dialogue.id == PLAYER_3_WEAPON_UPGRADE_NODE:
                        player_weapon2_upgrade(game=game, player_num=3)
                    elif scene_num == 1 and dialogue.id == PLAYER_4_WEAPON_UPGRADE_NODE:
                        player_weapon2_upgrade(game=game, player_num=4)

                    # TODO https://trello.com/c/b4qqBBgH/298-quest-assign-real-nodes
                    elif scene_num == 1 and dialogue.id == QUEST_1_NODE:
                        quest_choice_1(game=game)

                    elif scene_num == 1 and dialogue.id in [QUEST_2_NODE, QUEST_3_NODE]:
                        quest_choice_2_and_3(game=game)

                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_ALL_REST_NODE:
                        night_choice_all_rest(game=game, game_dialogue=game_dialogue)

                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_ROTATE_REST_NODE:
                        night_choice_rotate_watch(game=game, game_dialogue=game_dialogue)

                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_PLAYER_1_WATCH_NODE:
                        night_choice_one_player_watch(game=game, player_num=1, game_dialogue=game_dialogue)
                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_PLAYER_2_WATCH_NODE:
                        night_choice_one_player_watch(game=game, player_num=2, game_dialogue=game_dialogue)
                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_PLAYER_3_WATCH_NODE:
                        night_choice_one_player_watch(game=game, player_num=3, game_dialogue=game_dialogue)
                    elif scene_num == 1 and dialogue.id == NIGHT_DECISION_PLAYER_4_WATCH_NODE:
                        night_choice_one_player_watch(game=game, player_num=4, game_dialogue=game_dialogue)

                #########
                # Act 3 #
                #########
                if act == 3:
                    # TODO flesh out act 3
                    pass

            character_list = get_character_list(game=game)
            game_dialogue_progress_list = get_game_dialogue_progress_list(
                character_list=character_list,
                game_id=game_id,
                act=act,
                scene_num=scene_num,
            )
            next_dialogue_list = get_next_dialogue_list(
                game=game,
                game_dialogue_progress_list=game_dialogue_progress_list,
                character_list=character_list,
                act=act,
                scene_num=scene_num,
            )
            data = {
                "game_dialogue_progress_list": game_dialogue_progress_list,
                "next_dialogue_list": next_dialogue_list,
                "error": error_msg,
                "new_url": new_url,
            }
            return JsonResponse(data)

        else:
            character_list = get_character_list(game=game)
            game_dialogue_progress_list = get_game_dialogue_progress_list(
                character_list=character_list,
                game_id=game_id,
                act=act,
                scene_num=scene_num,
            )
            next_dialogue_list = get_next_dialogue_list(
                game=game,
                game_dialogue_progress_list=game_dialogue_progress_list,
                character_list=character_list,
                act=act,
                scene_num=scene_num,
            )
            data = {
                "game_dialogue_progress_list": game_dialogue_progress_list,
                "next_dialogue_list": next_dialogue_list,
                "error": "Something in the dialogue was not valid.",
                "new_url": "",
            }
            return JsonResponse(data)
    else:
        form = GameDialogueForm()

    character_list = get_character_list(game=game)
    game_dialogue_progress_list = get_game_dialogue_progress_list(
        character_list=character_list, game_id=game_id, act=act, scene_num=scene_num
    )
    next_dialogue_list = get_next_dialogue_list(
        game=game,
        game_dialogue_progress_list=game_dialogue_progress_list,
        character_list=character_list,
        act=act,
        scene_num=scene_num,
    )

    scene_image = SceneImage.objects.get(act=act, scene=scene_num)

    context = {
        "game_id": game_id,
        "game_dialogue_progress_list": game_dialogue_progress_list,
        "next_dialogue_list": next_dialogue_list,
        "form": form,
        "is_leader": is_leader,
        "act": act,
        "scene_num": scene_num,
        "scene_image": scene_image.image,
    }

    return render(request, "tavern_app/scene.html", context)


def scene_get_updates(request, game_id, act, number):
    scene_num = number
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    gamelocation = get_object_or_404(GameLocation, game=game)

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    new_url = ""

    # if they are not on this scene act/num - populate new_url so front end can redirect them
    if gamelocation.act != act or gamelocation.number != scene_num or gamelocation.location_type != "scene":
        new_url = reverse(
            "tavern_app:" + gamelocation.location_type,
            kwargs={
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            },
        )
    if game.game_over:
        new_url = reverse("tavern_app:gameover", kwargs={"game_id": game_id})

    character_list = get_character_list(game=game)
    game_dialogue_progress_list = get_game_dialogue_progress_list(
        character_list=character_list, game_id=game_id, act=act, scene_num=scene_num
    )
    next_dialogue_list = get_next_dialogue_list(
        game=game,
        game_dialogue_progress_list=game_dialogue_progress_list,
        character_list=character_list,
        act=act,
        scene_num=scene_num,
    )
    data = {
        "game_dialogue_progress_list": game_dialogue_progress_list,
        "next_dialogue_list": next_dialogue_list,
        "error": "",
        "new_url": new_url,
    }
    return JsonResponse(data)


def battle(request, game_id, act, number):
    battle_num = number
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    gamelocation = get_object_or_404(GameLocation, game=game)

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
        {
            "condition": game.game_over,
            "use_reverse": True,
            "redirect_url": "tavern_app:gameover",
            "kwargs": {"game_id": game_id}
        },
        {
            "condition": gamelocation.act != act or gamelocation.number != battle_num or gamelocation.location_type != "battle",
            "use_reverse": True,
            "redirect_url": "tavern_app:" + gamelocation.location_type,
            "kwargs": {
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            }
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    request_gameuser = GameUser.objects.get(game=game, user=request.user)
    gameusers = GameUser.objects.filter(game=game)
    gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle_num)

    if request.method == "POST":
        form = CombatLogForm(request.POST)

        if form.is_valid():
            has_error = False
            error_msg = ""

            ability = Ability.objects.get(pk=form.cleaned_data["ability"].id)

            unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
            is_request_user_turn = calc_is_request_user_turn(
                request_gameuser=request_gameuser, unit_turn=unit_turn
            )

            if not is_request_user_turn:
                has_error = True
                error_msg = "Can only cast abilities when it is your turn."

            if not has_error:
                if request_gameuser.current_mp < ability.mp_cost:
                    has_error = True
                    error_msg = "Not enough MP to cast that ability."

                if ability not in [
                    request_gameuser.ability_1,
                    request_gameuser.ability_2,
                    request_gameuser.ability_3,
                    request_gameuser.ability_4,
                ]:
                    has_error = True
                    error_msg = "You may only cast abilities that you know."

            if not has_error:
                # Damage Abilities
                if ability.is_heal is False and ability.is_buff is False:
                    # AOE Damage
                    if ability.is_aoe:
                        first_gameuser_attack = True
                        for gameenemy in gameenemies:
                            if gameenemy.current_hp > 0:
                                if first_gameuser_attack:
                                    gameuser_attack_single_gameenemy_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        gameenemy=gameenemy,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=True,
                                    )
                                    first_gameuser_attack = False
                                else:
                                    gameuser_attack_single_gameenemy_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        gameenemy=gameenemy,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=False,
                                    )
                    else:
                        # Single Target Damage
                        is_enemy_in_this_battle = (
                            True
                            if GameEnemy.objects.filter(
                                game=game,
                                pk=form.cleaned_data["gameenemy"].id,
                                act=act,
                                battle=battle_num,
                            )
                            else False
                        )
                        if not is_enemy_in_this_battle:
                            has_error = True
                            error_msg = "You may only attack enemies in this battle."

                        if not has_error:
                            gameenemy_target = GameEnemy.objects.get(
                                game=game, pk=form.cleaned_data["gameenemy"].id
                            )
                            if gameenemy_target.current_hp == 0:
                                error_msg = "Cannot single target enemy with 0 hp."
                            else:
                                gameuser_attack_single_gameenemy_and_save(
                                    game=game,
                                    gameuser=request_gameuser,
                                    gameenemy=gameenemy_target,
                                    ability=ability,
                                    unit_turn=unit_turn,
                                    act=act,
                                    battle=battle_num,
                                    deduct_mp=True,
                                )

                # Heal Abilities
                elif ability.is_heal:
                    # AOE Heal
                    if ability.is_aoe:
                        first_gameuser_heal = True
                        for gameuser in gameusers:
                            if gameuser.current_hp > 0:
                                if first_gameuser_heal:
                                    gameuser_heal_single_gameuser_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        defensive_gameuser_target=gameuser,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=True,
                                    )
                                    first_gameuser_heal = False
                                else:
                                    gameuser_heal_single_gameuser_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        defensive_gameuser_target=gameuser,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=False,
                                    )
                    else:
                        # Single Target Heal
                        is_player_in_this_game = (
                            True
                            if GameUser.objects.filter(
                                game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                            )
                            else False
                        )
                        if not is_player_in_this_game:
                            has_error = True
                            error_msg = "You may only heal players in this game."

                        if not has_error:
                            defensive_gameuser_target = GameUser.objects.get(
                                game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                            )
                            if defensive_gameuser_target.current_hp == 0:
                                error_msg = "Cannot single target heal player with 0 hp."
                            else:
                                gameuser_heal_single_gameuser_and_save(
                                    game=game,
                                    gameuser=request_gameuser,
                                    defensive_gameuser_target=defensive_gameuser_target,
                                    ability=ability,
                                    unit_turn=unit_turn,
                                    act=act,
                                    battle=battle_num,
                                    deduct_mp=True,
                                )

                # Buff Abilities
                elif ability.is_buff:
                    # AOE Buff
                    if ability.is_aoe:
                        first_gameuser_buff = True
                        for gameuser in gameusers:
                            if gameuser.current_hp > 0:
                                if first_gameuser_buff:
                                    gameuser_buff_single_gameuser_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        defensive_gameuser_target=gameuser,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=True,
                                    )
                                    first_gameuser_buff = False
                                else:
                                    gameuser_buff_single_gameuser_and_save(
                                        game=game,
                                        gameuser=request_gameuser,
                                        defensive_gameuser_target=gameuser,
                                        ability=ability,
                                        unit_turn=unit_turn,
                                        act=act,
                                        battle=battle_num,
                                        deduct_mp=False,
                                    )
                    else:
                        # Single Target Buff
                        is_player_in_this_game = (
                            True
                            if GameUser.objects.filter(
                                game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                            )
                            else False
                        )
                        if not is_player_in_this_game:
                            has_error = True
                            error_msg = "You may only buff players in this game."

                        if not has_error:
                            defensive_gameuser_target = GameUser.objects.get(
                                game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                            )
                            if defensive_gameuser_target.current_hp == 0:
                                error_msg = "Cannot single target buff player with 0 hp."
                            else:
                                gameuser_buff_single_gameuser_and_save(
                                    game=game,
                                    gameuser=request_gameuser,
                                    defensive_gameuser_target=defensive_gameuser_target,
                                    ability=ability,
                                    unit_turn=unit_turn,
                                    act=act,
                                    battle=battle_num,
                                    deduct_mp=True,
                                )

                calc_turns_and_execute_enemy_turns(act, battle_num, game, gameenemies, gameusers)
                check_and_handle_battle_over(game, act, battle_num)

            data = {
                "error": error_msg,
            }
            return JsonResponse(data)
        else:
            error_msg = "Something in combat form not valid."
            data = {
                "error": error_msg,
            }
            return JsonResponse(data)
    else:
        form = CombatLogForm()

    init_gameusers_current_battle_starting_stats(gameusers, act, battle_num)

    calc_turns_and_execute_enemy_turns(act, battle_num, game, gameenemies, gameusers)

    unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
    is_request_user_turn = calc_is_request_user_turn(
        request_gameuser=request_gameuser, unit_turn=unit_turn
    )

    context = {
        "game_id": game_id,
        "gameusers": gameusers,
        "gameenemies": gameenemies,
        "form": form,
        "request_gameuser": request_gameuser,
        "unit_turn": unit_turn,
        "is_request_user_turn": is_request_user_turn,
        "act": act,
        "battle_num": battle_num,
    }

    return render(request, "tavern_app/battle.html", context)


def battle_get_updates(request, game_id, act, number):
    battle_num = number
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    gamelocation = get_object_or_404(GameLocation, game=game)

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    new_url = ""

    # if they are not on this battle act/num - populate new_url so front end can redirect them
    if gamelocation.act != act or gamelocation.number != battle_num or gamelocation.location_type != "battle":
        new_url = reverse(
            "tavern_app:" + gamelocation.location_type,
            kwargs={
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            },
        )
    if game.game_over:
        new_url = reverse("tavern_app:gameover", kwargs={"game_id": game_id})

    game_combat_log = CombatLog.objects.filter(game=game, act=act, battle=battle_num)
    data_list = list(game_combat_log.values())

    gameuser_turn_queryset = GameTurnOrder.objects.filter(
        game=game, is_their_turn=True, gameuser__isnull=False
    )
    gameuser_turn_result = gameuser_turn_queryset.first()

    request_gameuser = GameUser.objects.get(game=game, user=request.user)

    if gameuser_turn_result:
        gameuser_turn_name = gameuser_turn_result.gameuser.name()
        is_request_user_turn = gameuser_turn_result.gameuser == request_gameuser
    else:
        gameuser_turn_name = ""
        is_request_user_turn = False

    data = {
        "game_combat_log": data_list,
        "gameuser_turn_name": gameuser_turn_name,
        "is_request_user_turn": is_request_user_turn,
        "error": "",
        "new_url": new_url,
    }
    return JsonResponse(data)


def gameover(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()
    gamelocation = get_object_or_404(GameLocation, game=game)

    criteria = [
        {
            "condition": not request.user.is_authenticated,
            "message_type": "info",
            "message": "Must be logged in to see a game. Log in or click the link below to register a new account.",
            "redirect_url": f"{reverse('login')}?next=/games/{game_id}",
        },
        {
            "condition": not is_user_in_game,
            "message_type": "error",
            "message": "Must be in the game to see it.",
            "redirect_url": "tavern_app:games",
        },
        {
            "condition": not game.game_over,
            "use_reverse": True,
            "redirect_url": "tavern_app:" + gamelocation.location_type,
            "kwargs": {
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            }
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    return render(request, 'tavern_app/gameover.html')
