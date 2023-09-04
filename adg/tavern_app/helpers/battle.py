from ..models import GameTurnOrder, CombatLog, GameEnemy, Ability, Game, GameUser
import random

def calc_and_save_turn_order(game: Game, gameusers, gameenemies) -> None:
    # get the game turn order. if it doesn't exist yet - populate the table and requery.
    game_turn_order = GameTurnOrder.objects.filter(game=game)
    if not game_turn_order:
        for gameuser in gameusers:
            gu_turn_order = GameTurnOrder(game=game, gameuser=gameuser, is_their_turn=False, accum_speed=gameuser.current_speed)
            gu_turn_order.save()
        for gameenemy in gameenemies:
            ge_turn_order = GameTurnOrder(game=game, gameenemy=gameenemy, is_their_turn=False, accum_speed=gameenemy.current_speed)
            ge_turn_order.save()
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

def gameuser_attack_single_gameenemy_and_save(game: Game, gameuser: GameUser, gameenemy: GameEnemy, ability: Ability, unit_turn: GameTurnOrder) -> None:
    combat_log = CombatLog(
        game = game,
        gameuser = gameuser,
        gameenemy = gameenemy,
        player_or_enemy_took_action = "player",
        ability = ability,
        damage = ability.max_damage, # for testing do the max damage. will update later
        unit_previous_hp = gameenemy.current_hp,
        unit_resulting_hp = gameenemy.current_hp - ability.max_damage,
        ability_mp_cost = ability.mp_cost,
        unit_previous_mp = gameuser.current_mp,
        unit_resulting_mp = gameuser.current_mp - ability.mp_cost,
        ability_min_damage = ability.min_damage,
        ability_max_damage = ability.max_damage,
        )
    combat_log.save()

    gameenemy.current_hp = gameenemy.current_hp - ability.max_damage
    gameenemy.save()

    gameuser.current_mp = gameuser.current_mp - ability.mp_cost
    gameuser.save()

    unit_turn.is_their_turn = False
    unit_turn.save()
    
def gameenemy_attack_single_gameuser_and_save(game: Game, gameuser: GameUser, gameenemy: GameEnemy, ability: Ability, unit_turn: GameTurnOrder) -> None:
    combat_log = CombatLog(
        game = game,
        gameuser = gameuser,
        gameenemy = gameenemy,
        player_or_enemy_took_action = "enemy",
        ability = ability,
        damage = ability.max_damage, # for testing do the max damage. will update later
        unit_previous_hp = gameuser.current_hp,
        unit_resulting_hp = gameuser.current_hp - ability.max_damage,
        ability_mp_cost = ability.mp_cost,
        unit_previous_mp = gameenemy.current_mp,
        unit_resulting_mp = gameenemy.current_mp - ability.mp_cost,
        ability_min_damage = ability.min_damage,
        ability_max_damage = ability.max_damage,
        )
    combat_log.save()

    gameuser.current_hp = gameuser.current_hp - ability.max_damage
    gameuser.save()

    gameenemy.current_mp = gameenemy.current_mp - ability.mp_cost
    gameenemy.save()

    unit_turn.is_their_turn = False
    unit_turn.save()

def enemey_choose_random_ability(gameenemy: GameEnemy) -> Ability:
    # TODO enemy must have mp needed for ability? or give them unlimited MP
    # TODO change to rand of 4 when we add fourth ability https://trello.com/c/jzFIFAaP/189-4-abilities-to-enemies-and-players-instead-of-3
    random_ability = "ability_" + str(random.randint(1, 3))
    return getattr(gameenemy.enemy, random_ability)

def enemey_choose_random_alive_target(gameusers) -> GameUser:
    gameuser_list = []
    for gameuser in gameusers:
        if gameuser.current_hp > 0:
            gameuser_list.append(gameuser)
    return random.choice(gameuser_list)