from ..models import GameTurnOrder, CombatLog, GameEnemy, Ability, Game, GameUser
import random

def calc_and_save_turn_order(game: Game, gameusers, gameenemies) -> None:
    # get the game turn order. if it doesn't exist yet - populate the table and requery.
    game_turn_order = GameTurnOrder.objects.filter(game=game)
    if not game_turn_order:
        for gameuser in gameusers:
            if gameuser.current_hp > 0:
                gu_turn_order = GameTurnOrder(game=game, gameuser=gameuser, is_their_turn=False, accum_speed=gameuser.current_speed)
                gu_turn_order.save()
        for gameenemy in gameenemies:
            if gameenemy.current_hp > 0:
                ge_turn_order = GameTurnOrder(game=game, gameenemy=gameenemy, is_their_turn=False, accum_speed=gameenemy.current_speed)
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
        if unit.is_their_turn == True:
            is_someones_turn = True
        if unit.accum_speed >= 100:
            is_someone_over_100 = True

    # if not someone's turn we need to run calculations to make it someone's turn
    if is_someones_turn == False:

        # nobody over 100 so we don't know who to give turn. increase all units accum_speed by current_speed until at least 1 is over 100.
        while is_someone_over_100 == False:
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
                if is_someones_turn == False:
                    unit.is_their_turn = True
                    unit.accum_speed = unit.accum_speed - 100
                    is_someones_turn = True
                    unit.save()
            unit.save()

def calc_is_request_user_turn(request_gameuser: GameUser, unit_turn: GameTurnOrder) -> bool:
    if unit_turn.gameuser:
        is_request_user_turn = True if unit_turn.gameuser == request_gameuser else False
    else:
        is_request_user_turn = False
    return is_request_user_turn

def gameuser_attack_single_gameenemy_and_save(game: Game, gameuser: GameUser, gameenemy: GameEnemy, ability: Ability, unit_turn: GameTurnOrder, act: int, battle: int) -> None:
    who_attacking = "player"
    calculated_damage = calculate_damage(gameuser=gameuser, gameenemy=gameenemy, ability=ability, who_attacking=who_attacking)
    
    combat_log = CombatLog(
        game = game,
        act=act,
        battle=battle,
        gameuser = gameuser,
        gameenemy = gameenemy,
        player_or_enemy_took_action = who_attacking,
        ability = ability,
        amount = calculated_damage,
        damage_or_heal_or_buff = "damage",
        )
    combat_log.save()

    gameenemy.current_hp = gameenemy.current_hp - calculated_damage
    if gameenemy.current_hp < 0:
        gameenemy.current_hp = 0
    gameenemy.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

def gameuser_deduct_ability_mp_and_save(gameuser: GameUser, ability: Ability):
    gameuser.current_mp -= ability.mp_cost
    gameuser.save()
    
def gameenemy_attack_single_gameuser_and_save(game: Game, gameuser: GameUser, gameenemy: GameEnemy, ability: Ability, unit_turn: GameTurnOrder, act: int, battle: int) -> None:
    who_attacking = "enemy"
    calculated_damage = calculate_damage(gameuser=gameuser, gameenemy=gameenemy, ability=ability, who_attacking=who_attacking)

    combat_log = CombatLog(
        game = game,
        act=act,
        battle=battle,
        gameuser = gameuser,
        gameenemy = gameenemy,
        player_or_enemy_took_action = who_attacking,
        ability = ability,
        amount = calculated_damage,
        damage_or_heal_or_buff = "damage",
        )
    combat_log.save()

    gameuser.current_hp = gameuser.current_hp - calculated_damage
    if gameuser.current_hp < 0:
        gameuser.current_hp = 0
    gameuser.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

def calculate_damage(gameuser: GameUser, gameenemy: GameEnemy, ability: Ability, who_attacking: str):
    if who_attacking == "player":
        attacker = gameuser
        target = gameenemy
    elif who_attacking == "enemy":
        attacker = gameenemy
        target = gameuser

    # TODO https://trello.com/c/ZBcEgLsh/164-combat-factor-in-type-strength-weakness-for-damage
    
    # TODO https://trello.com/c/acCnmIXe/165-combat-randomize-damage-between-min-max

    # TODO https://trello.com/c/OwzLDbD6/170-combat-factor-myst-reg-attack-and-defense

    print("attacker is: " + attacker.name())
    print("target is: " + target.name())
    print("target type is: " + target.unit_type().name)
    print("ability is: " + ability.name)
    print("ability type is: " + ability.type.name)

    final_damage = ability.max_damage
    print("final calculated damage is: " + str(final_damage))
    return final_damage
    

def enemey_choose_random_ability(gameenemy: GameEnemy) -> Ability:
    random_ability = "ability_" + str(random.randint(1, 4))
    return getattr(gameenemy.enemy, random_ability)

def enemey_choose_random_alive_target(gameusers) -> GameUser:
    gameuser_list = []
    for gameuser in gameusers:
        if gameuser.current_hp > 0:
            gameuser_list.append(gameuser)
    return random.choice(gameuser_list)

def gameuser_heal_single_gameuser_and_save(game: Game, gameuser: GameUser, defensive_gameuser_target: GameUser, ability: Ability, unit_turn: GameTurnOrder, act: int, battle: int) -> None:
    who_attacking = "player"
    calculated_healing = calculate_healing(gameuser=gameuser, defensive_gameuser_target=defensive_gameuser_target, ability=ability)

    combat_log = CombatLog(
        game = game,
        act=act,
        battle=battle,
        gameuser = gameuser,
        defensive_gameuser_target = defensive_gameuser_target,
        player_or_enemy_took_action = who_attacking,
        ability = ability,
        amount = calculated_healing,
        damage_or_heal_or_buff = "heal",
        )
    combat_log.save()

    defensive_gameuser_target.current_hp = defensive_gameuser_target.current_hp + calculated_healing
    if defensive_gameuser_target.current_hp > defensive_gameuser_target.current_max_hp:
        defensive_gameuser_target.current_hp = defensive_gameuser_target.current_max_hp
    defensive_gameuser_target.save()

    unit_turn.is_their_turn = False
    unit_turn.save()


def determine_type_strength_weakness(attack, attack_type_strength, attack_type_weakness, defense_type):
    """
    This function will be called when an ability is chosen to determine the ability type as compared to the opponent's
    role type. If the ability is a strength against the opponent's role type, it will be X% more effective. If it is a
    weakness, it will be Y% less effective. If there is no strength or weakness, the ability strength will not be
    changed.
    :param attack: either the with_gear_attack or with_gear_myst_attack depending on attack choice
    :param attack_type_strength: ability.type.strength
    :param attack_type_weakness: ability.type.weakness
    :param defense_type: target.role.type_id
    """
    attack_type_strength_weight = 1.25
    attack_type_weakness_weight = 0.75

    if defense_type == attack_type_strength:
        attack = attack * attack_type_strength_weight
    elif defense_type == attack_type_weakness:
        attack = attack * attack_type_weakness_weight

    return attack

def randomize_ability_strength():
    """
    This function will be called when an ability is chosen to randomize the strength. The float value returned should
    be applied to the ability strength determined in the main determine_ability_strength() function to provide some RNG.
    return: float value between -10% and +10%
    """
    return random.uniform(-0.1, 0.1)

def calculate_healing(gameuser: GameUser, defensive_gameuser_target: GameUser, ability: Ability):
    attacker = gameuser
    target = defensive_gameuser_target

    # TODO https://trello.com/c/6PCoXQ5O/196-combat-calculate-healing-done

    print("attacker is: " + attacker.name())
    print("target is: " + target.name())
    print("target type is: " + target.unit_type().name)
    print("ability is: " + ability.name)
    print("ability type is: " + ability.type.name)

    final_healing = ability.max_damage
    print("final calculated damage is: " + str(final_healing))
    return final_healing


def gameuser_buff_single_gameuser_and_save(game: Game, gameuser: GameUser, defensive_gameuser_target: GameUser, ability: Ability, unit_turn: GameTurnOrder, act: int, battle: int) -> None:
    who_attacking = "player"

    if ability.buff_hp_percent > 0:
        buffed_hp = defensive_gameuser_target.with_gear_hp + round(defensive_gameuser_target.with_gear_hp * ability.buff_hp_percent)
        if buffed_hp > defensive_gameuser_target.current_max_hp:
            hp_increase_delta = buffed_hp - defensive_gameuser_target.current_max_hp
            defensive_gameuser_target.current_max_hp = buffed_hp
            defensive_gameuser_target.current_hp += hp_increase_delta

    if ability.buff_mp_percent > 0:
        buffed_mp = defensive_gameuser_target.with_gear_mp + round(defensive_gameuser_target.with_gear_mp * ability.buff_mp_percent)
        if buffed_mp > defensive_gameuser_target.current_max_mp:
            mp_increase_delta = buffed_mp - defensive_gameuser_target.current_max_mp
            defensive_gameuser_target.current_max_mp = buffed_mp
            defensive_gameuser_target.current_mp += mp_increase_delta

    if ability.buff_attack_percent > 0:
        buffed_attack = defensive_gameuser_target.with_gear_attack + round(defensive_gameuser_target.with_gear_attack * ability.buff_attack_percent)
        if buffed_attack > defensive_gameuser_target.current_attack:
            defensive_gameuser_target.current_attack = buffed_attack

    if ability.buff_defense_percent > 0:
        buffed_defense = defensive_gameuser_target.with_gear_defense + round(defensive_gameuser_target.with_gear_defense * ability.buff_defense_percent)
        if buffed_defense > defensive_gameuser_target.current_defense:
            defensive_gameuser_target.current_defense = buffed_defense

    if ability.buff_myst_attack_percent > 0:
        buffed_myst_attack = defensive_gameuser_target.with_gear_myst_attack + round(defensive_gameuser_target.with_gear_myst_attack * ability.buff_myst_attack_percent)
        if buffed_myst_attack > defensive_gameuser_target.current_myst_attack:
            defensive_gameuser_target.current_myst_attack = buffed_myst_attack

    if ability.buff_myst_defense_percent > 0:
        buffed_myst_defense = defensive_gameuser_target.with_gear_myst_defense + round(defensive_gameuser_target.with_gear_myst_defense * ability.buff_myst_defense_percent)
        if buffed_myst_defense > defensive_gameuser_target.current_myst_defense:
            defensive_gameuser_target.current_myst_defense = buffed_myst_defense

    if ability.buff_speed_percent > 0:
        buffed_speed = defensive_gameuser_target.with_gear_speed + round(defensive_gameuser_target.with_gear_speed * ability.buff_speed_percent)
        if buffed_speed > defensive_gameuser_target.current_speed:
            defensive_gameuser_target.current_speed = buffed_speed

    defensive_gameuser_target.save()

    combat_log = CombatLog(
        game = game,
        act=act,
        battle=battle,
        gameuser = gameuser,
        defensive_gameuser_target = defensive_gameuser_target,
        player_or_enemy_took_action = who_attacking,
        ability = ability,
        amount = 0,
        damage_or_heal_or_buff = "buff",
        )
    combat_log.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

def is_any_player_alive(game: Game):
    return True if GameUser.objects.filter(game=game, current_hp__gt=0) else False