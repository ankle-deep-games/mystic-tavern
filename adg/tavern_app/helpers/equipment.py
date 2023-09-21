from ..models import GameUser, Armor

def gameuser_equip_armor(gameuser: GameUser, armor: Armor, slot: int):
    if slot == 1:
        gameuser.armor_1 = armor
    elif slot == 2:
        gameuser.amor_2 = armor
    elif slot == 3:
        gameuser.armor_3 = armor
    
    gameuser.save()
    

    # shared func with weapons to get all weapons and armor. tally up the total increases, and apply those increases