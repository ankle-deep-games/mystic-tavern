from ..models import GameUser, Armor

def gameuser_equip_armor(gameuser: GameUser, armor: Armor, slot: int):
    if slot == 1:
        gameuser.armor_1 = armor
    elif slot == 2:
        gameuser.armor_2 = armor
    elif slot == 3:
        gameuser.armor_3 = armor

    new_geared_defense = gameuser.role.start_defense
    if gameuser.armor_1:
        new_geared_defense += gameuser.armor_1.defense_mod
    if gameuser.armor_2:
        new_geared_defense += gameuser.armor_2.defense_mod
    if gameuser.armor_3:
        new_geared_defense += gameuser.armor_3.defense_mod
    gameuser.with_gear_defense = new_geared_defense
    gameuser.current_defense = new_geared_defense

    gameuser.save()

    # shared func with weapons to get all weapons and armor. tally up the total increases, and apply those increases