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
    Cons: 100% chance all gold stolen and 75% 1 random armor 3 to be stolen from 1 player
    Overwrites the dialogue node with the outcome.
    """
    # Initial part of the string
    event_description = ("The party all slept well overnight, restoring them to full HP and MP. However, in the night "
                         "they were robbed and all of their gold was stolen.")
    # first, calculate if we remove armor 3 from 1 player
    random_percent = random.random()
    if random_percent < 0.75:
        gameusers = GameUser.objects.filter(game=game)

        selected_gameuser = random.choice(gameusers[:4])

        event_description += f" And {selected_gameuser.name()} had their {selected_gameuser.armor_3.name} stolen."
        print(f"Action performed on {selected_gameuser}")
        gameuser_remove_armor(gameuser=selected_gameuser, slot=3)

        replaced_text = event_description
        game_dialogue.regex_replaced_text_or_empty = replaced_text
        game_dialogue.save()

        # TODO func to restore hp/mp to 100%

    else:
        # 25% chance of this block being executed
        print("Action did not happen.")
