from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, reverse
from django.shortcuts import render
from django.views.generic import CreateView

from .constants import QUEST_1_NODE, QUEST_2_NODE, QUEST_3_NODE, ROLE_GAME_PROGRESSION_DICT, END_OF_SCENE_1_NODES
from .forms import (
    CreateGameForm,
    JoinGameForm,
    RoleAssignmentForm,
    GameDialogueForm,
    StartGameForm,
    CombatLogForm,
)
from .helpers.ability import gameuser_grant_ability
from .helpers.battle import (
    gameuser_attack_single_gameenemy_and_save,
    gameuser_heal_single_gameuser_and_save,
    calc_is_request_user_turn,
    gameuser_buff_single_gameuser_and_save,
    calc_turns_and_execute_enemy_turns, check_and_handle_battle_over,
)
from .helpers.equipment import gameuser_equip_armor
from .helpers.game_setup import init_game_enemies
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
    Armor,
    SceneImage,
)


def homepage(request):
    criteria = [
        {
            'condition': request.user.is_authenticated,
            'redirect_url': "tavern_app:games",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    return render(request, 'tavern_app/home.html')


def seed(request):
    criteria = [
        {
            'condition': not request.user.is_superuser,
            'redirect_url': "tavern_app:games",
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
            'condition': not request.user.is_superuser,
            'redirect_url': "tavern_app:games",
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
            'condition': not request.user.is_authenticated,
            'message_type': 'error',
            'message': "Must be logged in to see games.",
            'redirect_url': "login",
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    game_list = []
    games_queryset = Game.objects.filter(game_over=False).annotate(num_players=Count("gameuser"))

    for game in games_queryset:
        is_user_in_game = (
            True if GameUser.objects.filter(game=game, user=request.user) else False
        )
        is_full = True if game.num_players == 4 else False
        is_started = game.game_started
        game_list.append(
            {
                "creator": game.creator,
                "id": game.id,
                "is_full": is_full,
                "is_started": is_started,
                "is_user_in_game": is_user_in_game,
                "name": game.name,
                "num_players": game.num_players,
            }
        )

    context = {
        "game_list": game_list,
    }

    return render(request, "tavern_app/games.html", context)


def join_game(request, pk):
    game = Game.objects.get(pk=pk)
    is_user_in_game = False
    if request.user.is_authenticated:
        is_user_in_game = GameUser.objects.filter(game=game, user=request.user).exists()

    criteria = [
        {
            'condition': not request.user.is_authenticated,
            'message_type': 'info',
            'message': "Must be logged in to join a game. Log in or click the link below to register a new account.",
            'redirect_url': f"{reverse('login')}?next=/games/{pk}",
        },
        {
            'condition': not Game.objects.filter(pk=pk).exists(),
            'message_type': 'error',
            'message': "Game does not exist.",
            'redirect_url': "tavern_app:games",
        },
        {
            'condition': is_user_in_game,
            'use_reverse': True,
            'redirect_url': "tavern_app:lobby",
            'kwargs': {"game_id": game.id},
        },
    ]
    redirect_response = check_redirect_criteria(request, criteria)
    if redirect_response:
        return redirect_response

    is_full = True if GameUser.objects.filter(game_id=pk).count() == 4 else False
    if is_full:
        messages.error(request, "Game is full.", extra_tags="alert alert-danger")
        return redirect("tavern_app:games")

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

    # else render form
    else:
        form = JoinGameForm()

    context = {
        "form": form,
    }

    return render(request, "tavern_app/join_game.html", context)


def lobby(request, game_id):
    if not request.user.is_authenticated:
        return redirect(reverse('tavern_app:join_game', kwargs={'pk': game_id}))

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        return redirect(reverse('tavern_app:join_game', kwargs={'pk': game_id}))

    game = Game.objects.get(id=game_id)

    if game.game_over:
        return redirect(reverse("tavern_app:gameover", kwargs={"game_id": game_id}))

    gameusers = GameUser.objects.filter(game_id=game_id)
    is_leader = (
        True
        if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user
        else False
    )
    any_player_not_ready = gameusers.filter(is_ready=False).exists()
    num_players_in_lobby = gameusers.count()

    if game.game_started:
        gamelocation = GameLocation.objects.get(game=game)
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
        "is_leader": is_leader,
        "any_player_not_ready": any_player_not_ready,
        "num_players_in_lobby": num_players_in_lobby,
        "form": form,
    }

    return render(request, "tavern_app/lobby.html", context)


def lobby_get_updates(request, game_id):
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

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

    def form_valid(self, form):
        game = form.save(commit=False)
        game.creator = self.request.user
        game.save()

        # Add the user who created the game to the gameuser table
        GameUser.objects.create(user=self.request.user, game=game)

        return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))


class BaseRoleAssignmentFormSet(BaseInlineFormSet):
    def clean(self):
        # TODO remove role assignments prints when done debugging
        # https://trello.com/c/9DhXpUWT/296-role-assignments-form-debug
        print("BaseRoleAssignmentFormSet CLEAN")
        """Custom formset-level validation."""
        if any(self.errors):
            print("BaseRoleAssignmentFormSet IF ANY ERRORS")
            # Don't perform validation if there are form errors already
            return

        roles = [form.cleaned_data.get('role') for form in self.forms if form.cleaned_data.get('role')]
        print("BaseRoleAssignmentFormSet ROLES")
        print(roles)
        if len(roles) != len(set(roles)):
            raise forms.ValidationError("Each player must have a unique role.")

        for form in self.forms:
            role = form.cleaned_data.get('role')
            gender = form.cleaned_data.get('gender')
            print(role)
            print(gender)

            if not role or not gender:
                raise forms.ValidationError("Every player must have a role and gender selected.")

        return super().clean()


def role_assignment(request, game_id):
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

    if game.game_over:
        return redirect(reverse("tavern_app:gameover", kwargs={"game_id": game_id}))

    if game.game_started:
        gamelocation = GameLocation.objects.get(game=game)
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

    is_leader = (
        True
        if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user
        else False
    )
    if not is_leader:
        messages.error(
            request, "Only party leader can assign roles.", extra_tags="alert alert-danger"
        )
        return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))

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
            print("FORMSET IS VALID")
            attack_ability = Ability.objects.get(pk=1)
            for form in formset:
                print(form)
                if form.cleaned_data:
                    print("CLEANED")
                    player = form.save(commit=False)  # Get the player object from the form
                    # Perform additional operations on the player based on the form data
                    player.current_hp = player.role.start_hp
                    player.current_max_hp = player.role.start_hp
                    player.current_mp = player.role.start_mp
                    player.current_max_mp = player.role.start_mp
                    player.current_attack = player.role.start_attack
                    player.current_defense = player.role.start_defense
                    player.current_myst_attack = player.role.start_myst_attack
                    player.current_myst_defense = player.role.start_myst_defense
                    player.current_speed = player.role.start_speed

                    player.with_gear_hp = player.role.start_hp
                    player.with_gear_mp = player.role.start_mp
                    player.with_gear_attack = player.role.start_attack
                    player.with_gear_defense = player.role.start_defense
                    player.with_gear_myst_attack = player.role.start_myst_attack
                    player.with_gear_myst_defense = player.role.start_myst_defense
                    player.with_gear_speed = player.role.start_speed

                    player.ability_1 = attack_ability

                    player.save()  # Save the updated player information

            formset.save()  # Save the formset data after updating the players
            return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))
    else:
        formset = role_assignment_form_set(instance=game, queryset=gameusers_queryset)

    return render(request, 'tavern_app/role_assignment.html', {'formset': formset})


def scene(request, game_id, act, number):
    scene_num = number
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

    if game.game_over:
        return redirect(reverse("tavern_app:gameover", kwargs={"game_id": game_id}))

    is_leader = (
        True
        if request.user == GameUser.objects.get(game_id=game_id, user=game.creator).user
        else False
    )

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
            gamelocation = GameLocation.objects.get(game=game)
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
                    # TODO https://trello.com/c/cS7s3OEs/217-combat-update-gamelocation-when-winning-and-losing-battles-depending-on-next-step-in-game
                    if scene_num == 1 and dialogue.id in END_OF_SCENE_1_NODES:
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

                    # TODO https://trello.com/c/WvyP6Teh/297-assign-weapons-and-armor-in-first-act-scene

                #########
                # Act 2 #
                #########
                if act == 2:
                    # TODO https://trello.com/c/b4qqBBgH/298-quest-assign-real-nodes
                    if scene_num == 1 and dialogue.id == QUEST_1_NODE:
                        # rewards: armor 2 and ability 3 for each player
                        gameusers = GameUser.objects.filter(game=game)
                        for gameuser in gameusers:
                            armor2 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor2'])
                            gameuser_equip_armor(gameuser=gameuser, armor=armor2, slot=2)
                            ability3 = Ability.objects.get(
                                name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['ability3'])
                            gameuser_grant_ability(gameuser=gameuser, ability=ability3, slot=3)

                    elif scene_num == 1 and dialogue.id in [QUEST_2_NODE, QUEST_3_NODE]:
                        # rewards: armor 2 and armor 3 for each player. choice 2 and 3 have same outcome.
                        gameusers = GameUser.objects.filter(game=game)
                        for gameuser in gameusers:
                            armor2 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor2'])
                            armor3 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor3'])
                            gameuser_equip_armor(gameuser=gameuser, armor=armor2, slot=2)
                            gameuser_equip_armor(gameuser=gameuser, armor=armor3, slot=3)

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

    # else render form
    else:
        form = GameDialogueForm()

    # redirect if they are not on this scene act/num
    gamelocation = GameLocation.objects.get(game=game)
    if gamelocation.act != act or gamelocation.number != scene_num or gamelocation.location_type != "scene":
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
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

    new_url = ""
    gamelocation = GameLocation.objects.get(game=game)

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
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

    if game.game_over:
        return redirect(reverse("tavern_app:gameover", kwargs={"game_id": game_id}))

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
                else:
                    messages.error(
                        request,
                        "It is not your turn to attack.",
                        extra_tags="alert alert-danger",
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

    # else render form
    else:
        form = CombatLogForm()

    # redirect if they are not on this battle act/num
    gamelocation = GameLocation.objects.get(game=game)
    if gamelocation.act != act or gamelocation.number != battle_num or gamelocation.location_type != "battle":
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

    # check if this battle starting hp/mp exist. if they don't, assign them.
    # these starting stats are used by frontend on first page load.
    for gameuser in gameusers:
        if gameuser.current_battle_act != act and gameuser.current_battle_number != battle_num:
            gameuser.current_battle_act = act
            gameuser.current_battle_number = battle_num
            gameuser.current_battle_starting_hp = gameuser.current_hp
            gameuser.current_battle_starting_hp_percent = round(
                (gameuser.current_battle_starting_hp / gameuser.with_gear_hp) * 100)
            gameuser.current_battle_starting_mp = gameuser.current_mp
            gameuser.current_battle_starting_mp_percent = round(
                (gameuser.current_battle_starting_mp / gameuser.with_gear_mp) * 100)
            gameuser.save()

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
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)

    new_url = ""
    gamelocation = GameLocation.objects.get(game=game)

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
    if not request.user.is_authenticated:
        return redirect("tavern_app:games")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=game_id)
    if not game.game_over:
        return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game_id}))

    return render(request, 'tavern_app/gameover.html')
