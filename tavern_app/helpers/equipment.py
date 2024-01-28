from ..models import GameUser, Armor, Weapon


def gameuser_equip_armor(gameuser: GameUser, armor: Armor, slot: int) -> None:
    gameuser = GameUser.objects.get(pk=gameuser.pk)
    if slot == 1:
        gameuser.armor_1 = armor
    elif slot == 2:
        gameuser.armor_2 = armor
    elif slot == 3:
        gameuser.armor_3 = armor

    gameuser_recalculate_gear_stats_and_save(gameuser=gameuser)


def gameuser_equip_weapon(gameuser: GameUser, weapon: Weapon) -> None:
    gameuser = GameUser.objects.get(pk=gameuser.pk)
    gameuser.weapon_1 = weapon

    gameuser_recalculate_gear_stats_and_save(gameuser=gameuser)


def gameuser_recalculate_gear_stats_and_save(gameuser: GameUser) -> None:
    new_geared_attack = gameuser.role.start_attack
    if gameuser.weapon_1:
        new_geared_attack += gameuser.weapon_1.attack_mod
    gameuser.with_gear_attack = new_geared_attack
    gameuser.current_attack = new_geared_attack

    new_geared_myst_attack = gameuser.role.start_myst_attack
    if gameuser.weapon_1:
        new_geared_myst_attack += gameuser.weapon_1.myst_attack_mod
    gameuser.with_gear_myst_attack = new_geared_myst_attack
    gameuser.current_myst_attack = new_geared_myst_attack

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

    new_geared_speed = gameuser.role.start_speed
    if gameuser.armor_1:
        new_geared_speed += gameuser.armor_1.speed_mod
    if gameuser.armor_2:
        new_geared_speed += gameuser.armor_2.speed_mod
    if gameuser.armor_3:
        new_geared_speed += gameuser.armor_3.speed_mod
    if gameuser.weapon_1:
        new_geared_speed += gameuser.weapon_1.speed_mod
    gameuser.with_gear_speed = new_geared_speed
    gameuser.current_speed = new_geared_speed

    new_geared_hp = gameuser.role.start_hp
    if gameuser.armor_1:
        new_geared_hp += gameuser.armor_1.hp_mod
    if gameuser.armor_2:
        new_geared_hp += gameuser.armor_2.hp_mod
    if gameuser.armor_3:
        new_geared_hp += gameuser.armor_3.hp_mod
    hp_delta = new_geared_hp - gameuser.current_max_hp
    gameuser.with_gear_hp = new_geared_hp
    gameuser.current_max_hp = new_geared_hp
    gameuser.current_hp += hp_delta

    new_geared_mp = gameuser.role.start_mp
    if gameuser.armor_1:
        new_geared_mp += gameuser.armor_1.mp_mod
    if gameuser.armor_2:
        new_geared_mp += gameuser.armor_2.mp_mod
    if gameuser.armor_3:
        new_geared_mp += gameuser.armor_3.mp_mod
    if gameuser.weapon_1:
        new_geared_mp += gameuser.weapon_1.mp_mod
    mp_delta = new_geared_mp - gameuser.current_max_mp
    gameuser.with_gear_mp = new_geared_mp
    gameuser.current_max_mp = new_geared_mp
    gameuser.current_mp += mp_delta

    gameuser.save()


def gameuser_remove_armor(gameuser: GameUser, slot: int) -> None:
    gameuser = GameUser.objects.get(pk=gameuser.pk)
    if slot == 1:
        gameuser.armor_1 = None
    elif slot == 2:
        gameuser.armor_2 = None
    elif slot == 3:
        gameuser.armor_3 = None

    gameuser_recalculate_gear_stats_and_save(gameuser=gameuser)
