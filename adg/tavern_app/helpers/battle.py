import random
from typing import Tuple

from ..models import GameTurnOrder, CombatLog, GameEnemy, Ability, Game, GameUser


def calc_and_save_turn_order(game: Game, gameusers, gameenemies) -> None:
    # get the game turn order. if it doesn't exist yet - populate the table and requery.
    game_turn_order = GameTurnOrder.objects.filter(game=game)
    if not game_turn_order:
        for gameuser in gameusers:
            if gameuser.current_hp > 0:
                gu_turn_order = GameTurnOrder(
                    game=game,
                    gameuser=gameuser,
                    is_their_turn=False,
                    accum_speed=gameuser.current_speed,
                )
                gu_turn_order.save()
        for gameenemy in gameenemies:
            if gameenemy.current_hp > 0:
                ge_turn_order = GameTurnOrder(
                    game=game,
                    gameenemy=gameenemy,
                    is_their_turn=False,
                    accum_speed=gameenemy.current_speed,
                )
                ge_turn_order.save()
        game_turn_order = GameTurnOrder.objects.filter(game=game)

    # check for units who have fainted by reaching 0 hp and remove them from the turn order
    any_units_fainted = False
    for unit in game_turn_order:
        if unit.gameuser:
            if unit.gameuser.current_hp == 0:
                any_units_fainted = True
                unit.delete()
        if unit.gameenemy:
            if unit.gameenemy.current_hp == 0:
                any_units_fainted = True
                unit.delete()
    if any_units_fainted:
        game_turn_order = GameTurnOrder.objects.filter(game=game)

    is_someones_turn = False
    is_someone_over_100 = False
    for unit in game_turn_order:
        if unit.is_their_turn:
            is_someones_turn = True
        if unit.accum_speed >= 100:
            is_someone_over_100 = True

    # if not someone's turn we need to run calculations to make it someone's turn
    if not is_someones_turn:
        # nobody over 100 so we don't know who to give turn. increase all units accum_speed by current_speed until at
        # least 1 is over 100.
        while not is_someone_over_100:
            for unit in game_turn_order:
                if unit.gameuser:
                    unit.accum_speed = unit.accum_speed + unit.gameuser.current_speed
                    if unit.accum_speed >= 100:
                        is_someone_over_100 = True
                if unit.gameenemy:
                    unit.accum_speed = unit.accum_speed + unit.gameenemy.current_speed
                    if unit.accum_speed >= 100:
                        is_someone_over_100 = True

        # now is_someone_over_100 is True
        for unit in game_turn_order:
            # only update reduce the speed and assign turn to 1 unit. save the rest
            if unit.accum_speed >= 100:
                if not is_someones_turn:
                    unit.is_their_turn = True
                    unit.accum_speed = unit.accum_speed - 100
                    is_someones_turn = True
                    unit.save()
            unit.save()


def calc_is_request_user_turn(
        request_gameuser: GameUser, unit_turn: GameTurnOrder
) -> bool:
    if unit_turn.gameuser:
        is_request_user_turn = True if unit_turn.gameuser == request_gameuser else False
    else:
        is_request_user_turn = False
    return is_request_user_turn


def gameuser_attack_single_gameenemy_and_save(
        game: Game,
        gameuser: GameUser,
        gameenemy: GameEnemy,
        ability: Ability,
        unit_turn: GameTurnOrder,
        act: int,
        battle: int,
        deduct_mp: bool,
) -> None:
    starting_gameusers = GameUser.objects.filter(game=game)
    starting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    starting_gameusers_json = list(
        starting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    starting_gameenemies_json = list(
        starting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    effectiveness_message, effectiveness_multiplier = calc_type_message_and_multiplier(ability, gameenemy.enemy.type.id)

    calculated_damage = calculate_damage(
        ability=ability,
        effectiveness_multiplier=effectiveness_multiplier,
    )

    if deduct_mp:
        gameuser.current_mp -= ability.mp_cost
        gameuser.save()

    gameenemy.current_hp = gameenemy.current_hp - calculated_damage
    if gameenemy.current_hp < 0:
        gameenemy.current_hp = 0
    gameenemy.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

    resulting_gameusers = GameUser.objects.filter(game=game)
    resulting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    resulting_gameusers_json = list(
        resulting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    resulting_gameenemies_json = list(
        resulting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    message = f"{gameuser.name()} used {ability.name} on {gameenemy.name()} for {calculated_damage} damage. {effectiveness_message}"

    combat_log = CombatLog(
        game=game,
        act=act,
        battle=battle,
        gameuser=gameuser,
        gameenemy=gameenemy,
        player_or_enemy_took_action="player",
        ability=ability,
        amount=calculated_damage,
        damage_or_heal_or_buff="damage",
        message=message,
        starting_gameusers_json=starting_gameusers_json,
        starting_gameenemies_json=starting_gameenemies_json,
        resulting_gameusers_json=resulting_gameusers_json,
        resulting_gameenemies_json=resulting_gameenemies_json,
    )
    combat_log.save()


def calc_type_message_and_multiplier(ability: Ability, defense_type_id: int) -> Tuple[str, float]:
    effectiveness_message = ''
    effectiveness_multiplier = 1.00
    attack_type_strength = ability.type.strength
    attack_type_weakness = ability.type.weakness

    if defense_type_id == attack_type_strength:
        effectiveness_message = "It was very effective."
        effectiveness_multiplier = 1.25

    elif defense_type_id == attack_type_weakness:
        effectiveness_message = "It was not very effective."
        effectiveness_multiplier = 0.75
    return effectiveness_message, effectiveness_multiplier


def gameenemy_attack_single_gameuser_and_save(
        game: Game,
        gameuser: GameUser,
        gameenemy: GameEnemy,
        ability: Ability,
        unit_turn: GameTurnOrder,
        act: int,
        battle: int,
) -> None:
    starting_gameusers = GameUser.objects.filter(game=game)
    starting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    starting_gameusers_json = list(
        starting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    starting_gameenemies_json = list(
        starting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    effectiveness_message, effectiveness_multiplier = calc_type_message_and_multiplier(ability, gameuser.role.type.id)

    calculated_damage = calculate_damage(
        ability=ability,
        effectiveness_multiplier=effectiveness_multiplier,
    )

    gameuser.current_hp = gameuser.current_hp - calculated_damage
    if gameuser.current_hp < 0:
        gameuser.current_hp = 0
    gameuser.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

    resulting_gameusers = GameUser.objects.filter(game=game)
    resulting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    resulting_gameusers_json = list(
        resulting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    resulting_gameenemies_json = list(
        resulting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    message = f"{gameenemy.name()} used {ability.name} on {gameuser.name()} for {calculated_damage} damage. {effectiveness_message}"

    combat_log = CombatLog(
        game=game,
        act=act,
        battle=battle,
        gameuser=gameuser,
        gameenemy=gameenemy,
        player_or_enemy_took_action="enemy",
        ability=ability,
        amount=calculated_damage,
        damage_or_heal_or_buff="damage",
        message=message,
        starting_gameusers_json=starting_gameusers_json,
        starting_gameenemies_json=starting_gameenemies_json,
        resulting_gameusers_json=resulting_gameusers_json,
        resulting_gameenemies_json=resulting_gameenemies_json,
    )
    combat_log.save()


def calculate_damage(ability: Ability, effectiveness_multiplier: float) -> int:
    # randomize damage between ability min/max
    num_between_min_max = random.randint(ability.min_damage, ability.max_damage)

    # TODO https://trello.com/c/OwzLDbD6/170-combat-factor-myst-reg-attack-and-defense
    # TODO https://trello.com/c/Pj9qSprE/254-combat-change-to-minamount-and-maxamount-in-the-model

    # modify damage depending on if ability type is effective, not effective, or neutral
    final_damage = round(num_between_min_max * effectiveness_multiplier)
    final_damage = int(final_damage)  # Convert the rounded value to an integer
    return final_damage


def enemy_choose_random_ability(gameenemy: GameEnemy) -> Ability:
    random_ability = "ability_" + str(random.randint(1, 4))
    return getattr(gameenemy.enemy, random_ability)


def enemy_choose_random_alive_target(gameusers) -> GameUser:
    gameuser_list = []
    for gameuser in gameusers:
        if gameuser.current_hp > 0:
            gameuser_list.append(gameuser)
    return random.choice(gameuser_list)


def gameuser_heal_single_gameuser_and_save(
        game: Game,
        gameuser: GameUser,
        defensive_gameuser_target: GameUser,
        ability: Ability,
        unit_turn: GameTurnOrder,
        act: int,
        battle: int,
        deduct_mp: bool,
) -> None:
    starting_gameusers = GameUser.objects.filter(game=game)
    starting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    starting_gameusers_json = list(
        starting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    starting_gameenemies_json = list(
        starting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    calculated_healing = calculate_healing(
        gameuser=gameuser,
        defensive_gameuser_target=defensive_gameuser_target,
        ability=ability,
    )

    if deduct_mp:
        gameuser.current_mp -= ability.mp_cost
        gameuser.save()

    # if healing themselves, requery since their MP just decreased
    if defensive_gameuser_target == gameuser:
        defensive_gameuser_target = GameUser.objects.get(pk=gameuser.pk)

    defensive_gameuser_target.current_hp = (
            defensive_gameuser_target.current_hp + calculated_healing
    )
    if defensive_gameuser_target.current_hp > defensive_gameuser_target.current_max_hp:
        defensive_gameuser_target.current_hp = defensive_gameuser_target.current_max_hp
    defensive_gameuser_target.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

    resulting_gameusers = GameUser.objects.filter(game=game)
    resulting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    resulting_gameusers_json = list(
        resulting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    resulting_gameenemies_json = list(
        resulting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    message = f"{gameuser.name()} used {ability.name} on {defensive_gameuser_target.name()} healing them for {calculated_healing}."

    combat_log = CombatLog(
        game=game,
        act=act,
        battle=battle,
        gameuser=gameuser,
        defensive_gameuser_target=defensive_gameuser_target,
        player_or_enemy_took_action="player",
        ability=ability,
        amount=calculated_healing,
        damage_or_heal_or_buff="heal",
        message=message,
        starting_gameusers_json=starting_gameusers_json,
        starting_gameenemies_json=starting_gameenemies_json,
        resulting_gameusers_json=resulting_gameusers_json,
        resulting_gameenemies_json=resulting_gameenemies_json,
    )
    combat_log.save()


def calculate_healing(
        gameuser: GameUser, defensive_gameuser_target: GameUser, ability: Ability
):
    # TODO https://trello.com/c/6PCoXQ5O/196-combat-calculate-healing-done
    final_healing = ability.max_damage
    return final_healing


def gameuser_buff_single_gameuser_and_save(
        game: Game,
        gameuser: GameUser,
        defensive_gameuser_target: GameUser,
        ability: Ability,
        unit_turn: GameTurnOrder,
        act: int,
        battle: int,
        deduct_mp: bool,
) -> None:
    starting_gameusers = GameUser.objects.filter(game=game)
    starting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    starting_gameusers_json = list(
        starting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    starting_gameenemies_json = list(
        starting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    if deduct_mp:
        gameuser.current_mp -= ability.mp_cost
        gameuser.save()

    # if buffing themselves, requery since their MP just decreased
    if defensive_gameuser_target == gameuser:
        defensive_gameuser_target = GameUser.objects.get(pk=gameuser.pk)

    if ability.buff_hp_percent > 0:
        buffed_hp = defensive_gameuser_target.with_gear_hp + round(
            defensive_gameuser_target.with_gear_hp * ability.buff_hp_percent
        )
        if buffed_hp > defensive_gameuser_target.current_max_hp:
            hp_increase_delta = buffed_hp - defensive_gameuser_target.current_max_hp
            defensive_gameuser_target.current_max_hp = buffed_hp
            defensive_gameuser_target.current_hp += hp_increase_delta

    if ability.buff_mp_percent > 0:
        buffed_mp = defensive_gameuser_target.with_gear_mp + round(
            defensive_gameuser_target.with_gear_mp * ability.buff_mp_percent
        )
        if buffed_mp > defensive_gameuser_target.current_max_mp:
            mp_increase_delta = buffed_mp - defensive_gameuser_target.current_max_mp
            defensive_gameuser_target.current_max_mp = buffed_mp
            defensive_gameuser_target.current_mp += mp_increase_delta

    if ability.buff_attack_percent > 0:
        buffed_attack = defensive_gameuser_target.with_gear_attack + round(
            defensive_gameuser_target.with_gear_attack * ability.buff_attack_percent
        )
        if buffed_attack > defensive_gameuser_target.current_attack:
            defensive_gameuser_target.current_attack = buffed_attack

    if ability.buff_defense_percent > 0:
        buffed_defense = defensive_gameuser_target.with_gear_defense + round(
            defensive_gameuser_target.with_gear_defense * ability.buff_defense_percent
        )
        if buffed_defense > defensive_gameuser_target.current_defense:
            defensive_gameuser_target.current_defense = buffed_defense

    if ability.buff_myst_attack_percent > 0:
        buffed_myst_attack = defensive_gameuser_target.with_gear_myst_attack + round(
            defensive_gameuser_target.with_gear_myst_attack
            * ability.buff_myst_attack_percent
        )
        if buffed_myst_attack > defensive_gameuser_target.current_myst_attack:
            defensive_gameuser_target.current_myst_attack = buffed_myst_attack

    if ability.buff_myst_defense_percent > 0:
        buffed_myst_defense = defensive_gameuser_target.with_gear_myst_defense + round(
            defensive_gameuser_target.with_gear_myst_defense
            * ability.buff_myst_defense_percent
        )
        if buffed_myst_defense > defensive_gameuser_target.current_myst_defense:
            defensive_gameuser_target.current_myst_defense = buffed_myst_defense

    if ability.buff_speed_percent > 0:
        buffed_speed = defensive_gameuser_target.with_gear_speed + round(
            defensive_gameuser_target.with_gear_speed * ability.buff_speed_percent
        )
        if buffed_speed > defensive_gameuser_target.current_speed:
            defensive_gameuser_target.current_speed = buffed_speed

    defensive_gameuser_target.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

    resulting_gameusers = GameUser.objects.filter(game=game)
    resulting_gameenemies = GameEnemy.objects.filter(game=game, act=act, battle=battle)
    resulting_gameusers_json = list(
        resulting_gameusers.values(
            "id", "current_hp", "current_max_hp", "current_mp", "current_max_mp"
        )
    )
    resulting_gameenemies_json = list(
        resulting_gameenemies.values("id", "current_hp", "enemy__start_hp")
    )

    message = f"{gameuser.name()} used {ability.name} on {defensive_gameuser_target.name()}. TODO buff what stats."

    combat_log = CombatLog(
        game=game,
        act=act,
        battle=battle,
        gameuser=gameuser,
        defensive_gameuser_target=defensive_gameuser_target,
        player_or_enemy_took_action="player",
        ability=ability,
        amount=0,
        damage_or_heal_or_buff="buff",
        message=message,
        starting_gameusers_json=starting_gameusers_json,
        starting_gameenemies_json=starting_gameenemies_json,
        resulting_gameusers_json=resulting_gameusers_json,
        resulting_gameenemies_json=resulting_gameenemies_json,
    )
    combat_log.save()


def is_any_player_alive(game: Game):
    return True if GameUser.objects.filter(game=game, current_hp__gt=0) else False


def calc_turns_and_execute_enemy_turns(act, battle_num, game, gameenemies, gameusers):
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

            calc_and_save_turn_order(
                game=game, gameusers=gameusers, gameenemies=gameenemies
            )

            # if enemy will go after current enemy - have that enemy attack by looping again
            is_enemy_turn_next = (
                True if GameTurnOrder.objects.get(game=game, is_their_turn=True).gameenemy is not None else False)
