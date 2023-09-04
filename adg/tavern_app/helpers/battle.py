from ..models import GameTurnOrder

def calc_and_save_turn_order(game, gameusers, gameenemies):
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