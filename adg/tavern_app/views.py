from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, reverse
from django.shortcuts import render
from django.views.generic import CreateView, FormView, TemplateView

from .forms import (
    CreateGameForm,
    JoinGameForm,
    RoleAssignmentForm,
    GameDialogueForm,
    StartGameForm,
    CombatLogForm,
)
from .helpers.battle import (
    calc_and_save_turn_order,
    gameuser_attack_single_gameenemy_and_save,
    gameenemy_attack_single_gameuser_and_save,
    enemy_choose_random_ability,
    enemy_choose_random_alive_target,
    gameuser_heal_single_gameuser_and_save,
    calc_is_request_user_turn,
    gameuser_buff_single_gameuser_and_save,
    is_any_player_alive,
)
from .helpers.equipment import gameuser_equip_armor, gameuser_equip_weapon
from .helpers.scene import (
    get_character_list,
    get_game_dialogue_progress_list,
    get_next_dialogue_list,
    plant_seed_decision,
)
from .helpers.seed import seed_data
from .models import (
    Game,
    GameUser,
    Dialogue,
    GameDialogue,
    Ability,
    Enemy,
    GameEnemy,
    CombatLog,
    GameLocation,
    GameTurnOrder,
    Armor,
    Weapon,
)


def simple_view():
    return HttpResponse(
        "LEEEROY JEEEEENKINS! LETS GOOOOOOO - David Lorenz & Jordan Philyaw - Hackathon May 2023"
    )


def seed(request):
    if not request.user.is_superuser:
        return redirect("tavern_app:home")

    seed_data()
    return render(request, "seed.html")


# /seed/game/:id - faster way to add 3 users to a game when creating games with dobby for manual testing
def add_three_users_to_game(request, game_id):
    if not request.user.is_superuser:
        return redirect("tavern_app:home")

    game = Game(pk=game_id)
    GameUser(game=game, user=User(pk=2)).save()
    GameUser(game=game, user=User(pk=3)).save()
    GameUser(game=game, user=User(pk=4)).save()
    return HttpResponse("3 users added to game " + str(game_id))


def equip_placeholder():
    gameuser = GameUser.objects.get(pk=6)
    armor = Armor.objects.get(pk=16)
    weapon = Weapon.objects.get(pk=1)
    gameuser_equip_armor(gameuser=gameuser, armor=armor, slot=3)
    gameuser_equip_weapon(gameuser=gameuser, weapon=weapon)
    return HttpResponse(
        "updated weapons and armor for "
        + gameuser.name()
        + " in game "
        + gameuser.game.name
        + ". check admin for that gameuser to see changes."
    )


class CreateOrJoinView(TemplateView):
    template_name = "tavern_app/home.html"


def games(request):
    if not request.user.is_authenticated:
        messages.error(
            request, "Must be logged in to see games.", extra_tags="alert alert-danger"
        )
        return redirect("login")

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
    if not request.user.is_authenticated:
        messages.error(
            request,
            "Must be logged in to join a game.",
            extra_tags="alert alert-danger",
        )
        return redirect("login")

    game_exists = Game.objects.filter(pk=pk).exists()
    if not game_exists:
        messages.error(request, "Game does not exist.", extra_tags="alert alert-danger")
        return redirect("tavern_app:games")

    game = Game.objects.get(pk=pk)
    is_user_in_game = (
        True if GameUser.objects.filter(game=game, user=request.user) else False
    )
    if is_user_in_game:
        return redirect(reverse("tavern_app:lobby", kwargs={"game_id": game.id}))

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
        messages.error(
            request, "Must be logged in to see a game.", extra_tags="alert alert-danger"
        )
        return redirect("login")

    if not GameUser.objects.filter(user_id=request.user, game_id=game_id).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    game = Game.objects.get(id=game_id)
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

            # TODO improve later: query all enemies and loop through adding them all into the game
            enemy1 = Enemy.objects.get(pk=1)
            enemy2 = Enemy.objects.get(pk=2)
            gameenemy1 = GameEnemy(
                game=game,
                enemy=enemy1,
                act=1,
                battle=1,
                current_hp=enemy1.start_hp,
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
                current_attack=enemy2.start_attack,
                current_defense=enemy2.start_defense,
                current_myst_attack=enemy2.start_myst_attack,
                current_myst_defense=enemy2.start_myst_defense,
                current_speed=enemy2.start_speed,
            )
            GameEnemy.objects.bulk_create(
                [
                    gameenemy1,
                    gameenemy2,
                ]
            )

            game.game_started = True
            game.save()

            gamelocation = GameLocation(
                game=game, act=1, location_type="scene", number=1
            )
            gamelocation.save()

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
        "game": game,
        "gameusers": gameusers,
        "is_leader": is_leader,
        "any_player_not_ready": any_player_not_ready,
        "num_players_in_lobby": num_players_in_lobby,
        "form": form,
    }

    return render(request, "tavern_app/lobby.html", context)


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


class RoleAssignmentView(FormView):
    template_name = "tavern_app/role_assignment.html"
    form_class = RoleAssignmentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["game_id"] = self.kwargs["game_id"]
        kwargs["num_players"] = GameUser.objects.filter(
            game_id=self.kwargs["game_id"]
        ).count()
        return kwargs

    def form_valid(self, form):
        game = Game.objects.get(pk=self.kwargs["game_id"])
        num_players = form.initial["num_players"]
        attack_ability = Ability.objects.get(pk=1)

        for i in range(1, num_players + 1):
            player_name = form.cleaned_data[f"player_{i}_name"]
            player_role = form.cleaned_data[f"player_{i}_role"]
            player_gender = form.cleaned_data[f"player_{i}_gender"]

            player = GameUser.objects.get(game=game, user__username=player_name)

            player.role = player_role
            player.gender = player_gender

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

            player.save()

        return super().form_valid(form)

    def get_success_url(self):
        game_id = self.kwargs["game_id"]
        return reverse("tavern_app:lobby", kwargs={"game_id": game_id})


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
                game_dialogue.save()

            if (
                    (act == 1 and scene_num == 1 and dialogue.id == 58)
                    or (act == 1 and scene_num == 1 and dialogue.id == 65)
                    or (act == 1 and scene_num == 1 and dialogue.id == 72)
            ):
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

            # TODO https://trello.com/c/BCQJFpKL/200-function-to-determine-ability-3-based-on-plant-the-seed-decision
            #  change act/scene/dialogue to execute at correct place adding here now as an example of how we'll
            #  execute decisions in dialogue when we get here we might add func params to plant_seed_decision func
            #  this approach will also be used for fork in road decision for forest/mountain choice. conditionally
            #  execute a scene helper func
            if act == 1 and scene_num == 1 and dialogue.id == 5:
                plant_seed_decision()

            character_list = get_character_list(game=game)
            game_dialogue_progress_list = get_game_dialogue_progress_list(
                character_list=character_list,
                game_id=game_id,
                act=act,
                scene_num=scene_num,
            )
            next_dialogue_list = get_next_dialogue_list(
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
    if (
            gamelocation.game.pk != game_id
            and gamelocation.act != act
            and gamelocation.number != scene_num
            or gamelocation.location_type != "scene"
    ):
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
        game_dialogue_progress_list=game_dialogue_progress_list,
        character_list=character_list,
        act=act,
        scene_num=scene_num,
    )

    # TODO https://trello.com/c/oL6acc6m/127-end-of-act-1-scene-1-final-button-goes-to-battle

    context = {
        "game_id": game_id,
        "game_dialogue_progress_list": game_dialogue_progress_list,
        "next_dialogue_list": next_dialogue_list,
        "form": form,
        "is_leader": is_leader,
        "act": act,
        "scene_num": scene_num,
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
    if (
            gamelocation.game.pk != game_id
            and gamelocation.act != act
            and gamelocation.number != scene_num
            or gamelocation.location_type != "scene"
    ):
        new_url = reverse(
            "tavern_app:" + gamelocation.location_type,
            kwargs={
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            },
        )

    character_list = get_character_list(game=game)
    game_dialogue_progress_list = get_game_dialogue_progress_list(
        character_list=character_list, game_id=game_id, act=act, scene_num=scene_num
    )
    next_dialogue_list = get_next_dialogue_list(
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

    game = Game.objects.get(pk=game_id)

    if not GameUser.objects.filter(user_id=request.user, game=game).exists():
        messages.error(
            request, "Must be in the game to see it.", extra_tags="alert alert-danger"
        )
        return redirect("tavern_app:games")

    request_gameuser = GameUser.objects.get(game=game, user=request.user)
    gameusers = GameUser.objects.filter(game=game)
    gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle_num)

    if request.method == "POST":
        form = CombatLogForm(request.POST)

        if form.is_valid():
            ability = Ability.objects.get(pk=form.cleaned_data["ability"].id)

            unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
            is_request_user_turn = calc_is_request_user_turn(
                request_gameuser=request_gameuser, unit_turn=unit_turn
            )

            if request_gameuser.current_mp < ability.mp_cost:
                messages.error(
                    request,
                    "Not enough MP to cast that ability.",
                    extra_tags="alert alert-danger",
                )
                # TODO update redirect to current battle
                return redirect(
                    reverse(
                        "tavern_app:battle",
                        kwargs={"game_id": game.id, "act": 1, "number": 1},
                    )
                )

            if ability not in [
                request_gameuser.ability_1,
                request_gameuser.ability_2,
                request_gameuser.ability_3,
                request_gameuser.ability_4,
            ]:
                messages.error(
                    request,
                    "You may only cast abilities that you know.",
                    extra_tags="alert alert-danger",
                )
                # TODO update redirect to current battle
                return redirect(
                    reverse(
                        "tavern_app:battle",
                        kwargs={"game_id": game.id, "act": 1, "number": 1},
                    )
                )

            if (
                    is_request_user_turn
                    and ability.is_heal is False
                    and ability.is_buff is False
            ):
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
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

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
                    messages.error(
                        request,
                        "You may only attack enemies in this battle.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

                gameenemy_target = GameEnemy.objects.get(
                    game=game, pk=form.cleaned_data["gameenemy"].id
                )
                if gameenemy_target.current_hp == 0:
                    messages.error(
                        request,
                        "Cannot single target enemy with 0 hp.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

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

            elif is_request_user_turn and ability.is_heal:
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
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

                # Single Target Heal
                is_player_in_this_game = (
                    True
                    if GameUser.objects.filter(
                        game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                    )
                    else False
                )
                if not is_player_in_this_game:
                    messages.error(
                        request,
                        "You may only heal players in this game.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

                defensive_gameuser_target = GameUser.objects.get(
                    game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                )
                if defensive_gameuser_target.current_hp == 0:
                    messages.error(
                        request,
                        "Cannot single target heal player with 0 hp.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )
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

            elif is_request_user_turn and ability.is_buff:
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
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

                # Single Target Buff
                is_player_in_this_game = (
                    True
                    if GameUser.objects.filter(
                        game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                    )
                    else False
                )
                if not is_player_in_this_game:
                    messages.error(
                        request,
                        "You may only buff players in this game.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )

                defensive_gameuser_target = GameUser.objects.get(
                    game=game, pk=form.cleaned_data["defensive_gameuser_target"].id
                )
                if defensive_gameuser_target.current_hp == 0:
                    messages.error(
                        request,
                        "Cannot single target buff player with 0 hp.",
                        extra_tags="alert alert-danger",
                    )
                    # TODO update redirect to current battle
                    return redirect(
                        reverse(
                            "tavern_app:battle",
                            kwargs={"game_id": game.id, "act": 1, "number": 1},
                        )
                    )
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

            # TODO update redirect to current battle
            return redirect(
                reverse(
                    "tavern_app:battle",
                    kwargs={"game_id": game.id, "act": 1, "number": 1},
                )
            )
        else:
            messages.error(
                request,
                "Something in combat form not valid",
                extra_tags="alert alert-danger",
            )
            # TODO return JSONRESPONSE on success and error of form submit

    # else render form
    else:
        form = CombatLogForm()

    calc_and_save_turn_order(game=game, gameusers=gameusers, gameenemies=gameenemies)

    if GameTurnOrder.objects.get(game=game, is_their_turn=True).gameenemy:
        is_enemy_turn_next = True
        while is_enemy_turn_next:
            if not is_any_player_alive(game=game):
                break

            unit_turn = GameTurnOrder.objects.get(game=game, is_their_turn=True)
            gameenemy = unit_turn.gameenemy
            ability = enemy_choose_random_ability(gameenemy)

            # Enemies can only AOE or single target damage.
            # Enemies cannot heal or buff.
            # Enemies do not use MP.
            if ability.is_aoe:
                # AOE Damage
                for gameuser in gameusers:
                    if gameuser.current_hp > 0:
                        gameenemy_attack_single_gameuser_and_save(
                            game=game,
                            gameuser=gameuser,
                            gameenemy=gameenemy,
                            ability=ability,
                            unit_turn=unit_turn,
                            act=act,
                            battle=battle_num,
                        )
            else:
                # Single Target Damage
                gameuser_target = enemy_choose_random_alive_target(gameusers=gameusers)
                gameenemy_attack_single_gameuser_and_save(
                    game=game,
                    gameuser=gameuser_target,
                    gameenemy=gameenemy,
                    ability=ability,
                    unit_turn=unit_turn,
                    act=act,
                    battle=battle_num,
                )
                # TODO change log message from ability.max_damage to real damage. and then later change UI entirely

            calc_and_save_turn_order(
                game=game, gameusers=gameusers, gameenemies=gameenemies
            )

            # if enemy will go after current enemy - have that enemy attack by looping again
            is_enemy_turn_next = (
                True if GameTurnOrder.objects.get(game=game, is_their_turn=True).gameenemy is not None else False)

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

    # TODO prototype getting in here for proof of concept of drunk guys defeating players and then going to act 1
    #  scene 2 this will change when battles use javascript (including other non party leaders redirecting) still
    #  need to add defeating enemies and redirecting. related
    #  https://trello.com/c/cS7s3OEs/217-combat-update-gamelocation-when-winning-and-loosing-battles-depending-on
    #  -next-step-in-game
    gamelocation = GameLocation.objects.get(game=game)
    if not is_any_player_alive(game=game):
        if act == 1 and battle_num == 1:
            gamelocation.location_type = "scene"
            gamelocation.number = 2
            gamelocation.save()

            # TODO change to real dialogue
            act_one_scene_two_dialogue = GameDialogue(
                game=game, dialogue=Dialogue.objects.get(pk=4)
            )
            act_one_scene_two_dialogue.save()

            # TODO delete turn orders

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
            # TODO new_url = reverse("tavern_app:" + gamelocation.location_type, kwargs={'game_id': game.id,
            #  'act': gamelocation.act, 'number': gamelocation.number})

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
    if (
            gamelocation.game.pk != game_id
            and gamelocation.act != act
            and gamelocation.number != battle_num
            or gamelocation.location_type != "battle"
    ):
        new_url = reverse(
            "tavern_app:" + gamelocation.location_type,
            kwargs={
                "game_id": game.id,
                "act": gamelocation.act,
                "number": gamelocation.number,
            },
        )

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
