import random

from tavern_app.constants import ROLE_GAME_PROGRESSION_DICT
from tavern_app.helpers.ability import gameuser_grant_ability
from tavern_app.helpers.equipment import gameuser_equip_armor, gameuser_remove_armor
from tavern_app.models import GameUser, Armor, Ability, Game, GameDialogue


def quest_choice_1(game: Game) -> None:
    """rewards: armor 2 and ability 3 for each player"""
    gameusers = GameUser.objects.filter(game=game)
    for gameuser in gameusers:
        armor2 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor2'])
        gameuser_equip_armor(gameuser=gameuser, armor=armor2, slot=2)
        ability3 = Ability.objects.get(
            name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['ability3'])
        gameuser_grant_ability(gameuser=gameuser, ability=ability3, slot=3)


def quest_choice_2_and_3(game: Game) -> None:
    """rewards: armor 2 and armor 3 for each player. choice 2 and 3 have same outcome."""
    gameusers = GameUser.objects.filter(game=game)
    for gameuser in gameusers:
        armor2 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor2'])
        armor3 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[gameuser.role.name]['armor3'])
        gameuser_equip_armor(gameuser=gameuser, armor=armor2, slot=2)
        gameuser_equip_armor(gameuser=gameuser, armor=armor3, slot=3)


def night_choice_all_rest(game: Game, game_dialogue: GameDialogue):
    """
    100% rest.
    Pros: Full HP/MP restoration for all party members.
    Cons: 100% chance all gold stolen and 75% 1 random armor 3 to be stolen from 1 player.
    Overwrites the dialogue node with the outcome.
    """
    # Initial string
    event_description = ("The party all slept well overnight, restoring them to full HP and MP. However, in the night "
                         "they were robbed and all of their gold was stolen.")

    # first calculate if we remove armor 3 from a random player
    random_percent = random.random()
    if random_percent < 0.75:
        gameusers = GameUser.objects.filter(game=game)
        selected_gameuser = random.choice(gameusers[:4])
        event_description += f" And {selected_gameuser.name()} had their {selected_gameuser.armor_3.name} stolen."
        game_dialogue.regex_replaced_text_or_empty = event_description
        game_dialogue.save()

        gameuser_remove_armor(gameuser=selected_gameuser, slot=3)  # TODO verify this correctly reduces stats

    # then restore all gameusers to full hp/mp
    for gameuser in gameusers:
        restore_gameuser_hp_and_mp_x_percent(gameuser=gameuser, restore_percent=1.0)


def night_choice_rotate_rest(game: Game, game_dialogue: GameDialogue):
    """
    Partial rest. Everyone rotates a watch shift.
    Pros: Partial (50%) HP/MP restoration for all party members
    Cons: Not 100% restoration.
    Overwrites the dialogue node with the outcome.
    """
    event_description = "The party rotated watch. Everyone slept part of the night and restored some HP and MP."
    game_dialogue.regex_replaced_text_or_empty = event_description
    game_dialogue.save()

    gameusers = GameUser.objects.filter(game=game)
    for gameuser in gameusers:
        restore_gameuser_hp_and_mp_x_percent(gameuser=gameuser, restore_percent=0.5)


def restore_gameuser_hp_and_mp_x_percent(gameuser: GameUser, restore_percent: float):
    gameuser = GameUser.objects.get(pk=gameuser.pk)

    if restore_percent == 1.0:
        gameuser.current_hp = gameuser.current_max_hp
        gameuser.current_mp = gameuser.current_max_mp
        gameuser.save()
    else:
        hp_increase = round(gameuser.with_gear_hp * restore_percent)
        if (gameuser.current_hp + hp_increase) > gameuser.current_max_hp:
            gameuser.current_hp = gameuser.current_max_hp
        else:
            gameuser.current_hp += hp_increase

        mp_increase = round(gameuser.with_gear_mp * restore_percent)
        if (gameuser.current_mp + mp_increase) > gameuser.current_max_mp:
            gameuser.current_mp = gameuser.current_max_mp
        else:
            gameuser.current_mp += mp_increase

        gameuser.save()
