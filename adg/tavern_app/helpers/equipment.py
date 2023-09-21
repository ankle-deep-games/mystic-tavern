from ..models import GameUser, Armor, Weapon

def gameuser_equip_armor(gameuser: GameUser, armor: Armor, slot: int):
    if slot == 1:
        gameuser.armor_1 = armor
    elif slot == 2:
        gameuser.armor_2 = armor
    elif slot == 3:
        gameuser.armor_3 = armor
    
    gameuser_recalculate_gear_stats_and_save(gameuser=gameuser)

def gameuser_equip_weapon(gameuser: GameUser, weapon: Weapon, slot: int):
    if slot == 1:
        gameuser.weapon_1 = weapon
    elif slot == 2:
        gameuser.weapon_2 = weapon
    elif slot == 3:
        gameuser.weapon_3 = weapon
    
    gameuser_recalculate_gear_stats_and_save(gameuser=gameuser)

def gameuser_recalculate_gear_stats_and_save(gameuser: GameUser):
    new_geared_defense = gameuser.role.start_defense
    if gameuser.armor_1:
        new_geared_defense += gameuser.armor_1.defense_mod
    if gameuser.armor_2:
        new_geared_defense += gameuser.armor_2.defense_mod
    if gameuser.armor_3:
        new_geared_defense += gameuser.armor_3.defense_mod
    gameuser.with_gear_defense = new_geared_defense
    gameuser.current_defense = new_geared_defense

    new_geared_myst_defense = gameuser.role.start_myst_defense
    if gameuser.armor_1:
        new_geared_myst_defense += gameuser.armor_1.myst_defense_mod
    if gameuser.armor_2:
        new_geared_myst_defense += gameuser.armor_2.myst_defense_mod
    if gameuser.armor_3:
        new_geared_myst_defense += gameuser.armor_3.myst_defense_mod
    gameuser.with_gear_myst_defense = new_geared_myst_defense
    gameuser.current_myst_defense = new_geared_myst_defense

    gameuser.save()

    # shared func with weapons to get all weapons and armor. tally up the total increases, and apply those increases