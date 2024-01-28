from .ability import gameuser_grant_ability
from .equipment import gameuser_equip_armor, gameuser_equip_weapon
from ..constants import ROLE_GAME_PROGRESSION_DICT
from ..forms import BaseRoleAssignmentFormSet
from ..models import Enemy, GameEnemy, Game, Ability, GameUser, Armor, Weapon


def init_game_enemies(game: Game) -> None:
    #########
    # Act 1 #
    #########
    drunk_man_1 = Enemy.objects.get(pk=1)
    drunk_man_2 = Enemy.objects.get(pk=2)

    # Battle 1: Drunk Man 1 and 2 first battle where they win
    gameenemy1 = GameEnemy(
        game=game,
        enemy=drunk_man_1,
        act=1,
        battle=1,
        current_hp=drunk_man_1.start_hp,
        current_attack=drunk_man_1.start_attack,
        current_defense=drunk_man_1.start_defense,
        current_myst_attack=drunk_man_1.start_myst_attack,
        current_myst_defense=drunk_man_1.start_myst_defense,
        current_speed=drunk_man_1.start_speed,
    )
    gameenemy2 = GameEnemy(
        game=game,
        enemy=drunk_man_2,
        act=1,
        battle=1,
        current_hp=drunk_man_2.start_hp,
        current_attack=drunk_man_2.start_attack,
        current_defense=drunk_man_2.start_defense,
        current_myst_attack=drunk_man_2.start_myst_attack,
        current_myst_defense=drunk_man_2.start_myst_defense,
        current_speed=drunk_man_2.start_speed,
    )

    # Battle 2: new Drunk Man 1 and 2 second battle
    gameenemy3 = GameEnemy(
        game=game,
        enemy=drunk_man_1,
        act=1,
        battle=2,
        current_hp=drunk_man_1.start_hp,
        current_attack=drunk_man_1.start_attack,
        current_defense=drunk_man_1.start_defense,
        current_myst_attack=drunk_man_1.start_myst_attack,
        current_myst_defense=drunk_man_1.start_myst_defense,
        current_speed=drunk_man_1.start_speed,
    )
    gameenemy4 = GameEnemy(
        game=game,
        enemy=drunk_man_2,
        act=1,
        battle=2,
        current_hp=drunk_man_2.start_hp,
        current_attack=drunk_man_2.start_attack,
        current_defense=drunk_man_2.start_defense,
        current_myst_attack=drunk_man_2.start_myst_attack,
        current_myst_defense=drunk_man_2.start_myst_defense,
        current_speed=drunk_man_2.start_speed,
    )

    #########
    # Act 2 #
    #########
    arachnid_sovereign = Enemy.objects.get(pk=3)
    arachnid_minion = Enemy.objects.get(pk=4)

    # Battle 1: Arachnid Minion, Arachnid Sovereign, Arachnid Minion
    gameenemy5 = GameEnemy(
        game=game,
        enemy=arachnid_minion,
        act=2,
        battle=1,
        current_hp=arachnid_minion.start_hp,
        current_attack=arachnid_minion.start_attack,
        current_defense=arachnid_minion.start_defense,
        current_myst_attack=arachnid_minion.start_myst_attack,
        current_myst_defense=arachnid_minion.start_myst_defense,
        current_speed=arachnid_minion.start_speed,
    )
    gameenemy6 = GameEnemy(
        game=game,
        enemy=arachnid_sovereign,
        act=2,
        battle=1,
        current_hp=arachnid_sovereign.start_hp,
        current_attack=arachnid_sovereign.start_attack,
        current_defense=arachnid_sovereign.start_defense,
        current_myst_attack=arachnid_sovereign.start_myst_attack,
        current_myst_defense=arachnid_sovereign.start_myst_defense,
        current_speed=arachnid_sovereign.start_speed,
    )
    gameenemy7 = GameEnemy(
        game=game,
        enemy=arachnid_minion,
        act=2,
        battle=1,
        current_hp=arachnid_minion.start_hp,
        current_attack=arachnid_minion.start_attack,
        current_defense=arachnid_minion.start_defense,
        current_myst_attack=arachnid_minion.start_myst_attack,
        current_myst_defense=arachnid_minion.start_myst_defense,
        current_speed=arachnid_minion.start_speed,
    )

    #########
    # Act 3 #
    #########
    primordial_anomaly = Enemy.objects.get(pk=5)
    luminar_sentinel = Enemy.objects.get(pk=6)
    umbral_harbinger = Enemy.objects.get(pk=7)
    granite_warden = Enemy.objects.get(pk=8)
    sylvan_enchanter = Enemy.objects.get(pk=9)
    galewing_shaman = Enemy.objects.get(pk=10)

    # Battle 1: Galewing Shaman and Sylvan Enchanter
    gameenemy8 = GameEnemy(
        game=game,
        enemy=galewing_shaman,
        act=3,
        battle=1,
        current_hp=galewing_shaman.start_hp,
        current_attack=galewing_shaman.start_attack,
        current_defense=galewing_shaman.start_defense,
        current_myst_attack=galewing_shaman.start_myst_attack,
        current_myst_defense=galewing_shaman.start_myst_defense,
        current_speed=galewing_shaman.start_speed,
    )
    gameenemy9 = GameEnemy(
        game=game,
        enemy=sylvan_enchanter,
        act=3,
        battle=1,
        current_hp=sylvan_enchanter.start_hp,
        current_attack=sylvan_enchanter.start_attack,
        current_defense=sylvan_enchanter.start_defense,
        current_myst_attack=sylvan_enchanter.start_myst_attack,
        current_myst_defense=sylvan_enchanter.start_myst_defense,
        current_speed=sylvan_enchanter.start_speed,
    )

    # Battle 2: Umbral Harbinger, Luminar Sentinal, Granite Warden
    gameenemy10 = GameEnemy(
        game=game,
        enemy=umbral_harbinger,
        act=3,
        battle=2,
        current_hp=umbral_harbinger.start_hp,
        current_attack=umbral_harbinger.start_attack,
        current_defense=umbral_harbinger.start_defense,
        current_myst_attack=umbral_harbinger.start_myst_attack,
        current_myst_defense=umbral_harbinger.start_myst_defense,
        current_speed=umbral_harbinger.start_speed,
    )
    gameenemy11 = GameEnemy(
        game=game,
        enemy=luminar_sentinel,
        act=3,
        battle=2,
        current_hp=luminar_sentinel.start_hp,
        current_attack=luminar_sentinel.start_attack,
        current_defense=luminar_sentinel.start_defense,
        current_myst_attack=luminar_sentinel.start_myst_attack,
        current_myst_defense=luminar_sentinel.start_myst_defense,
        current_speed=luminar_sentinel.start_speed,
    )
    gameenemy12 = GameEnemy(
        game=game,
        enemy=granite_warden,
        act=3,
        battle=2,
        current_hp=granite_warden.start_hp,
        current_attack=granite_warden.start_attack,
        current_defense=granite_warden.start_defense,
        current_myst_attack=granite_warden.start_myst_attack,
        current_myst_defense=granite_warden.start_myst_defense,
        current_speed=granite_warden.start_speed,
    )

    # Battle 3: Primordal Anomaly
    gameenemy13 = GameEnemy(
        game=game,
        enemy=primordial_anomaly,
        act=3,
        battle=3,
        current_hp=primordial_anomaly.start_hp,
        current_attack=primordial_anomaly.start_attack,
        current_defense=primordial_anomaly.start_defense,
        current_myst_attack=primordial_anomaly.start_myst_attack,
        current_myst_defense=primordial_anomaly.start_myst_defense,
        current_speed=primordial_anomaly.start_speed,
    )

    GameEnemy.objects.bulk_create(
        [
            gameenemy1,
            gameenemy2,
            gameenemy3,
            gameenemy4,
            gameenemy5,
            gameenemy6,
            gameenemy7,
            gameenemy8,
            gameenemy9,
            gameenemy10,
            gameenemy11,
            gameenemy12,
            gameenemy13,
        ]
    )


def role_assignment_init_player_stats(formset: BaseRoleAssignmentFormSet) -> None:
    print("FORMSET IS VALID")
    attack_ability = Ability.objects.get(pk=1)
    for form in formset:
        print(form)
        if form.cleaned_data:
            print("CLEANED")
            player = form.save(commit=False)  # Get the player object from the form

            player.current_hp = player.role.start_hp
            player.current_max_hp = player.role.start_hp
            player.current_mp = player.role.start_mp
            player.current_max_mp = player.role.start_mp
            player.current_attack = player.role.start_attack
            player.current_defense = player.role.start_defense
            player.current_myst_attack = player.role.start_myst_attack
            player.current_myst_defense = player.role.start_myst_defense
            player.current_speed = player.role.start_speed

            player.with_gear_hp = player.role.start_hp
            player.with_gear_mp = player.role.start_mp
            player.with_gear_attack = player.role.start_attack
            player.with_gear_defense = player.role.start_defense
            player.with_gear_myst_attack = player.role.start_myst_attack
            player.with_gear_myst_defense = player.role.start_myst_defense
            player.with_gear_speed = player.role.start_speed

            player.ability_1 = attack_ability

            player.save()  # Save the updated player information


def equip_player_with_starting_weapon1_armor1_ability2(game: Game, player_num: int) -> None:
    gameusers = GameUser.objects.filter(game=game)
    player_queryset_index = player_num - 1
    selected_gameuser = gameusers[player_queryset_index]
    armor1 = Armor.objects.get(name=ROLE_GAME_PROGRESSION_DICT[selected_gameuser.role.name]['armor1'])
    gameuser_equip_armor(gameuser=selected_gameuser, armor=armor1, slot=1)
    weapon1 = Weapon.objects.get(name=ROLE_GAME_PROGRESSION_DICT[selected_gameuser.role.name]['weapon1'])
    gameuser_equip_weapon(gameuser=selected_gameuser, weapon=weapon1)
    ability2 = Ability.objects.get(name=ROLE_GAME_PROGRESSION_DICT[selected_gameuser.role.name]['ability2'])
    gameuser_grant_ability(gameuser=selected_gameuser, ability=ability2, slot=2)
