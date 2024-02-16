from django.contrib.auth.models import User

from ..constants import DIVINE_LIGHT, GALE_FURY, SHADOW_BLAST, ATTACK, SHIELD_BASH, SHATTER_SHOT, ANTHEM_OF_VALOR, \
    DIVINE_STRIKE, SHADOW_VOLLEY, ENCHANTED_GROVE, RESONANT_STONES, HOLY_WRATH, GROVES_VENGEANCE, SANCTUARY, \
    ARCANE_DARKNESS, ETHEREAL_CRESCENDO, WOOD_STAFF, WOOD_SWORD, WOOD_BOW, WOOD_FLUTE, LONGSWORD, LONGBOW, IVORY_ROD, \
    OBSIDIAN_WAND, MELODIOUS_LUTE, CLOTH_TUNIC, RADIANT_CUIRASS, ELVEN_WINDWRAP, ARCHMAGES_VESTMENTS, \
    SORCERERS_ROBES, MAESTROS_TAILCOAT, VALOR_SHIELD, FALCONERS_BRACERS, CELESTIAL_CIRCLET, SHADOWWEAVE_CAPE, \
    HARMONISTS_CUMMERBUND
from ..models import (
    Game,
    GameUser,
    Role,
    Gender,
    Dialogue,
    NPC,
    Type,
    Weapon,
    Armor,
    Ability,
    Enemy,
    SceneImage,
)


def seed_data():
    # users are special because they get created with a hashed password with create_user
    user1 = User.objects.create_user(
        username="john", email="jlennon@beatles.com", password="imagine"
    )
    user2 = User.objects.create_user(
        username="paul", email="pmccartney@beatles.com", password="let it be"
    )
    user3 = User.objects.create_user(
        username="george", email="gharrison@beatles.com", password="my sweet lord"
    )
    user4 = User.objects.create_user(
        username="ringo", email="rstarr@beatles.com", password="yellow submarine"
    )
    user5 = User.objects.create_user(
        username="eleanor", email="erigby@beatles.com", password="lonely people"
    )
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user5.save()

    # games
    game1 = Game(
        name="Game Seed 1",
        creator=user1,
        game_started=False,
        game_over=False,
        password="apple",
    )
    game2 = Game(
        name="Game Seed 2",
        creator=user2,
        game_started=False,
        game_over=False,
        password="banana",
    )
    Game.objects.bulk_create(
        [
            game1,
            game2,
        ]
    )

    # types
    type_light = Type(name="Light", strength=2, weakness=5)
    type_dark = Type(name="Dark", strength=3, weakness=1)
    type_stone = Type(name="Stone", strength=4, weakness=2)
    type_forest = Type(name="Forest", strength=5, weakness=3)
    type_wind = Type(name="Wind", strength=1, weakness=4)
    type_normal = Type(name="Normal", strength=6, weakness=6)
    Type.objects.bulk_create(
        [
            type_light,
            type_dark,
            type_stone,
            type_forest,
            type_wind,
            type_normal,
        ]
    )

    # scene images
    scene_image1 = SceneImage(act=1, scene=1, image="setting-alley.png")
    SceneImage.objects.bulk_create(
        [
            scene_image1,
        ]
    )

    # roles
    role1 = Role(
        name="WHITEMAGE",
        display_name="White Mage",
        type=type_light,
        start_hp=100,
        start_mp=100,
        start_attack=10,
        start_defense=20,
        start_myst_attack=15,
        start_myst_defense=20,
        start_speed=25,
    )
    role2 = Role(
        name="BLACKMAGE",
        display_name="Black Mage",
        type=type_dark,
        start_hp=80,
        start_mp=120,
        start_attack=15,
        start_defense=10,
        start_myst_attack=35,
        start_myst_defense=10,
        start_speed=30,
    )
    role3 = Role(
        name="PALADIN",
        display_name="Paladin",
        type=type_stone,
        start_hp=120,
        start_mp=80,
        start_attack=20,
        start_defense=30,
        start_myst_attack=10,
        start_myst_defense=20,
        start_speed=20,
    )
    role4 = Role(
        name="ARCHER",
        display_name="Archer",
        type=type_forest,
        start_hp=110,
        start_mp=90,
        start_attack=35,
        start_defense=15,
        start_myst_attack=10,
        start_myst_defense=10,
        start_speed=30,
    )
    role5 = Role(
        name="BARD",
        display_name="Bard",
        type=type_wind,
        start_hp=90,
        start_mp=110,
        start_attack=20,
        start_defense=20,
        start_myst_attack=20,
        start_myst_defense=20,
        start_speed=20,
    )
    Role.objects.bulk_create(
        [
            role1,
            role2,
            role3,
            role4,
            role5,
        ]
    )

    # genders
    gender1 = Gender(name="MALE")
    gender2 = Gender(name="FEMALE")
    Gender.objects.bulk_create(
        [
            gender1,
            gender2,
        ]
    )

    # weapons
    weapon1 = Weapon(
        name=WOOD_STAFF, attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5
    )
    weapon2 = Weapon(
        name=WOOD_SWORD, attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5
    )
    weapon3 = Weapon(
        name=WOOD_BOW, attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5
    )
    weapon4 = Weapon(
        name=WOOD_FLUTE, attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5
    )
    weapon5 = Weapon(
        name=LONGSWORD, attack_mod=26, myst_attack_mod=12, speed_mod=10, mp_mod=12
    )
    weapon6 = Weapon(
        name=LONGBOW, attack_mod=26, myst_attack_mod=10, speed_mod=12, mp_mod=12
    )
    weapon7 = Weapon(
        name=IVORY_ROD, attack_mod=10, myst_attack_mod=20, speed_mod=10, mp_mod=20
    )
    weapon8 = Weapon(
        name=OBSIDIAN_WAND, attack_mod=10, myst_attack_mod=22, speed_mod=10, mp_mod=18
    )
    weapon9 = Weapon(
        name=MELODIOUS_LUTE,
        attack_mod=10,
        myst_attack_mod=20,
        speed_mod=12,
        mp_mod=18,
    )
    Weapon.objects.bulk_create(
        [
            weapon1,
            weapon2,
            weapon3,
            weapon4,
            weapon5,
            weapon6,
            weapon7,
            weapon8,
            weapon9,
        ]
    )

    # armor
    armor1 = Armor(
        name=CLOTH_TUNIC,
        defense_mod=5,
        myst_defense_mod=5,
        speed_mod=5,
        hp_mod=5,
        mp_mod=5,
    )
    armor2 = Armor(
        name=RADIANT_CUIRASS,
        defense_mod=20,
        myst_defense_mod=20,
        speed_mod=10,
        hp_mod=15,
        mp_mod=10,
    )
    armor3 = Armor(
        name=ELVEN_WINDWRAP,
        defense_mod=15,
        myst_defense_mod=15,
        speed_mod=15,
        hp_mod=15,
        mp_mod=15,
    )
    armor4 = Armor(
        name=ARCHMAGES_VESTMENTS,
        defense_mod=18,
        myst_defense_mod=20,
        speed_mod=10,
        hp_mod=12,
        mp_mod=15,
    )
    armor5 = Armor(
        name=SORCERERS_ROBES,
        defense_mod=10,
        myst_defense_mod=20,
        speed_mod=15,
        hp_mod=10,
        mp_mod=20,
    )
    armor6 = Armor(
        name=MAESTROS_TAILCOAT,
        defense_mod=10,
        myst_defense_mod=20,
        speed_mod=15,
        hp_mod=10,
        mp_mod=20,
    )
    armor7 = Armor(
        name=VALOR_SHIELD,
        defense_mod=20,
        myst_defense_mod=25,
        speed_mod=15,
        hp_mod=30,
        mp_mod=23,
    )
    armor8 = Armor(
        name=FALCONERS_BRACERS,
        defense_mod=20,
        myst_defense_mod=20,
        speed_mod=30,
        hp_mod=25,
        mp_mod=18,
    )
    armor9 = Armor(
        name=CELESTIAL_CIRCLET,
        defense_mod=25,
        myst_defense_mod=18,
        speed_mod=20,
        hp_mod=25,
        mp_mod=25,
    )
    armor10 = Armor(
        name=SHADOWWEAVE_CAPE,
        defense_mod=25,
        myst_defense_mod=20,
        speed_mod=20,
        hp_mod=20,
        mp_mod=28,
    )
    armor11 = Armor(
        name=HARMONISTS_CUMMERBUND,
        defense_mod=25,
        myst_defense_mod=20,
        speed_mod=23,
        hp_mod=20,
        mp_mod=25,
    )
    Armor.objects.bulk_create(
        [
            armor1,
            armor2,
            armor3,
            armor4,
            armor5,
            armor6,
            armor7,
            armor8,
            armor9,
            armor10,
            armor11,
        ]
    )

    # abilities
    # Tier 1
    ability1 = Ability(
        name=ATTACK,
        description="A basic single-target physical attack that inflicts low damage without consuming MP.",
        type=type_normal,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=1,
        max_amount=5,
    )
    # Tier 2
    ability2 = Ability(
        name=SHIELD_BASH,
        description="A physical attack that deals low damage to one enemy by thrusting a shield into the enemy.",
        type=type_stone,
        mp_cost=5,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )
    ability3 = Ability(
        name=SHATTER_SHOT,
        description="A precise single-target physical attack that delivers medium damage to one enemy with a "
                    "precisely aimed arrow.",
        type=type_forest,
        mp_cost=5,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )
    ability4 = Ability(
        name=DIVINE_LIGHT,
        description="A single-target healing spell that provides a gentle, low-level healing effect to one ally with "
                    "a radiant burst of light.",
        type=type_light,
        mp_cost=10,
        is_myst_attack=True,
        is_heal=True,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )
    ability5 = Ability(
        name=SHADOW_BLAST,
        description="A focused single-target attack that inflicts medium damage on one enemy through a powerful surge "
                    "of arcane energy.",
        type=type_dark,
        mp_cost=10,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )
    ability6 = Ability(
        name=ANTHEM_OF_VALOR,
        description="Empowers a single ally with a medium physical attack boost and a defensive buff, enhancing their"
                    "strength and resilience.",
        type=type_wind,
        mp_cost=10,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=True,
        buff_attack_percent=0.1,
        buff_defense_percent=0.1,
    )
    # Tier 3
    ability7 = Ability(
        name=DIVINE_STRIKE,
        description="Launches a medium mystic attack, harnessing the power of light to strike a single target with "
                    "celestial force.",
        type=type_light,
        mp_cost=30,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )
    ability8 = Ability(
        name=SHADOW_VOLLEY,
        description="Fires a barrage of dark-infused arrows in a medium mystic attack that targets a single enemy.",
        type=type_dark,
        mp_cost=30,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )
    ability9 = Ability(
        name=ENCHANTED_GROVE,
        description="Evokes the magic of the forest with a medium mystic attack, creating an enchanting grove that "
                    "envelops a single target.",
        type=type_forest,
        mp_cost=20,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )
    ability10 = Ability(
        name=RESONANT_STONES,
        description="Conjures a medium mystic attack with resonating stones, creating a harmonious symphony that "
                    "engulfs a single target.",
        type=type_stone,
        mp_cost=20,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )
    ability11 = Ability(
        name=GALE_FURY,
        description="Commands a medium mystic attack imbued with the tempest's might, releasing a raging windstorm "
                    "upon a single target, inflicting swirling damage.",
        type=type_wind,
        mp_cost=20,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )
    # Tier 4
    ability12 = Ability(
        name=HOLY_WRATH,
        description="Summons divine fury, delivering a devastating high physical attack that channels holy energy to "
                    "smite multiple targets with righteous force.",
        type=type_stone,
        mp_cost=15,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=30,
        max_amount=45,
    )
    ability13 = Ability(
        name=GROVES_VENGEANCE,
        description="Harnesses the fury of the forest, unleashing a potent high physical attack that embodies the "
                    "wrath of nature upon multiple targets.",
        type=type_forest,
        mp_cost=15,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=30,
        max_amount=45,
    )
    ability14 = Ability(
        name=SANCTUARY,
        description="Invokes a healing haven, granting a substantial high-level heal that envelops multiple targets "
                    "in a protective aura of rejuvenation.",
        type=type_light,
        mp_cost=30,
        is_myst_attack=True,
        is_heal=True,
        is_aoe=True,
        is_buff=False,
        min_amount=30,
        max_amount=45,
    )
    ability15 = Ability(
        name=ARCANE_DARKNESS,
        description="Conjures dark mystic forces, casting a formidable high mystic attack that shrouds multiple "
                    "targets in shadowy, unpredictable energies.",
        type=type_dark,
        mp_cost=30,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=30,
        max_amount=45,
    )
    ability16 = Ability(
        name=ETHEREAL_CRESCENDO,
        description="Orchestrates a symphony of power, bestowing a robust buff to all stats upon multiple targets, "
                    "elevating them to an ethereal peak of strength and grace.",
        type=type_wind,
        mp_cost=30,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=True,
        is_buff=True,
        buff_hp_percent=0.1,
        buff_mp_percent=0.1,
        buff_attack_percent=0.1,
        buff_defense_percent=0.1,
        buff_myst_attack_percent=0.1,
        buff_myst_defense_percent=0.1,
        buff_speed_percent=0.1,
    )

    # Enemy Abilities
    ability17 = Ability(
        name="Drunken Haymaker",
        description="N/A",
        type=type_light,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=10,
    )

    ability18 = Ability(
        name="Tankard Thrash",
        description="N/A",
        type=type_light,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=5,
        max_amount=10,
    )

    ability19 = Ability(
        name="Ethereal Smite",
        description="N/A",
        type=type_light,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )

    ability20 = Ability(
        name="Bar Brawl Slam",
        description="N/A",
        type=type_dark,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=10,
    )

    ability21 = Ability(
        name="Tavern Tumble",
        description="N/A",
        type=type_dark,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=5,
        max_amount=10,
    )

    ability22 = Ability(
        name="Abyssal Gloom",
        description="N/A",
        type=type_dark,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=5,
        max_amount=15,
    )

    ability23 = Ability(
        name="Pincer Assault",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )

    ability24 = Ability(
        name="Veil of Vines",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )

    ability25 = Ability(
        name="Arboreal Pulse",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=50,
    )

    ability26 = Ability(
        name="Venomous Bite",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=15,
        max_amount=30,
    )

    ability27 = Ability(
        name="Obliteration",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=30,
        max_amount=50,
    )

    ability28 = Ability(
        name="Eclipse",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=30,
        max_amount=50,
    )

    ability29 = Ability(
        name="Desolation",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=30,
        max_amount=50,
    )

    ability30 = Ability(
        name="Chaos",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=True,
        is_buff=False,
        min_amount=30,
        max_amount=75,
    )

    ability31 = Ability(
        name="Dawnblade",
        description="N/A",
        type=type_light,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability32 = Ability(
        name="Angelic Conduit",
        description="N/A",
        type=type_light,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability33 = Ability(
        name="Voidclaw",
        description="N/A",
        type=type_dark,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability34 = Ability(
        name="Cataclysm",
        description="N/A",
        type=type_dark,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability35 = Ability(
        name="Stonebreaker",
        description="N/A",
        type=type_stone,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability36 = Ability(
        name="Eruption",
        description="N/A",
        type=type_stone,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability37 = Ability(
        name="Brambles",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability38 = Ability(
        name="Verdant Whisper",
        description="N/A",
        type=type_forest,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability39 = Ability(
        name="Whirlwind Assault",
        description="N/A",
        type=type_wind,
        mp_cost=0,
        is_myst_attack=False,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    ability40 = Ability(
        name="Aetheric Tempest",
        description="N/A",
        type=type_wind,
        mp_cost=0,
        is_myst_attack=True,
        is_heal=False,
        is_aoe=False,
        is_buff=False,
        min_amount=25,
        max_amount=50,
    )

    Ability.objects.bulk_create(
        [
            ability1,
            ability2,
            ability3,
            ability4,
            ability5,
            ability6,
            ability7,
            ability8,
            ability9,
            ability10,
            ability11,
            ability12,
            ability13,
            ability14,
            ability15,
            ability16,
            ability17,
            ability18,
            ability19,
            ability20,
            ability21,
            ability22,
            ability23,
            ability24,
            ability25,
            ability26,
            ability27,
            ability28,
            ability29,
            ability30,
            ability31,
            ability32,
            ability33,
            ability34,
            ability35,
            ability36,
            ability37,
            ability38,
            ability39,
            ability40,
        ]
    )

    # gameuser
    gameuser1 = GameUser(
        game=game1,
        user=user1,
        role=role1,
        gender=gender1,
        is_ready=True,
        current_hp=role1.start_hp,
        current_max_hp=role1.start_hp,
        current_mp=role1.start_mp,
        current_max_mp=role1.start_mp,
        current_attack=role1.start_attack,
        current_defense=role1.start_defense,
        current_myst_attack=role1.start_myst_attack,
        current_myst_defense=role1.start_myst_defense,
        current_speed=role1.start_speed,
        with_gear_hp=role1.start_hp,
        with_gear_mp=role1.start_mp,
        with_gear_attack=role1.start_attack,
        with_gear_defense=role1.start_defense,
        with_gear_myst_attack=role1.start_myst_attack,
        with_gear_myst_defense=role1.start_myst_defense,
        with_gear_speed=role1.start_speed,
        ability_1=ability1,
        ability_2=ability4,
        ability_3=ability9,
        ability_4=ability14,
    )
    gameuser2 = GameUser(
        game=game1,
        user=user2,
        role=role2,
        gender=gender2,
        is_ready=True,
        current_hp=role2.start_hp,
        current_max_hp=role2.start_hp,
        current_mp=role2.start_mp,
        current_max_mp=role2.start_mp,
        current_attack=role2.start_attack,
        current_defense=role2.start_defense,
        current_myst_attack=role2.start_myst_attack,
        current_myst_defense=role2.start_myst_defense,
        current_speed=role2.start_speed,
        with_gear_hp=role2.start_hp,
        with_gear_mp=role2.start_mp,
        with_gear_attack=role2.start_attack,
        with_gear_defense=role2.start_defense,
        with_gear_myst_attack=role2.start_myst_attack,
        with_gear_myst_defense=role2.start_myst_defense,
        with_gear_speed=role2.start_speed,
        ability_1=ability1,
        ability_2=ability5,
        ability_3=ability10,
        ability_4=ability15,
    )
    gameuser3 = GameUser(
        game=game1,
        user=user3,
        role=role3,
        gender=gender2,
        is_ready=True,
        current_hp=role3.start_hp,
        current_max_hp=role3.start_hp,
        current_mp=role3.start_mp,
        current_max_mp=role3.start_mp,
        current_attack=role3.start_attack,
        current_defense=role3.start_defense,
        current_myst_attack=role3.start_myst_attack,
        current_myst_defense=role3.start_myst_defense,
        current_speed=role3.start_speed,
        with_gear_hp=role3.start_hp,
        with_gear_mp=role3.start_mp,
        with_gear_attack=role3.start_attack,
        with_gear_defense=role3.start_defense,
        with_gear_myst_attack=role3.start_myst_attack,
        with_gear_myst_defense=role3.start_myst_defense,
        with_gear_speed=role3.start_speed,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability7,
        ability_4=ability12,
    )
    gameuser4 = GameUser(
        game=game1,
        user=user4,
        role=role4,
        gender=gender1,
        is_ready=True,
        current_hp=role4.start_hp,
        current_max_hp=role4.start_hp,
        current_mp=role4.start_mp,
        current_max_mp=role4.start_mp,
        current_attack=role4.start_attack,
        current_defense=role4.start_defense,
        current_myst_attack=role4.start_myst_attack,
        current_myst_defense=role4.start_myst_defense,
        current_speed=role4.start_speed,
        with_gear_hp=role4.start_hp,
        with_gear_mp=role4.start_mp,
        with_gear_attack=role4.start_attack,
        with_gear_defense=role4.start_defense,
        with_gear_myst_attack=role4.start_myst_attack,
        with_gear_myst_defense=role4.start_myst_defense,
        with_gear_speed=role4.start_speed,
        ability_1=ability1,
        ability_2=ability3,
        ability_3=ability8,
        ability_4=ability13,
    )
    gameuser5 = GameUser(
        game=game2,
        user=user2,
        role=role2,
        gender=gender1,
        is_ready=True,
        current_hp=role2.start_hp,
        current_max_hp=role2.start_hp,
        current_mp=role2.start_mp,
        current_max_mp=role2.start_mp,
        current_attack=role2.start_attack,
        current_defense=role2.start_defense,
        current_myst_attack=role2.start_myst_attack,
        current_myst_defense=role2.start_myst_defense,
        current_speed=role2.start_speed,
        with_gear_hp=role2.start_hp,
        with_gear_mp=role2.start_mp,
        with_gear_attack=role2.start_attack,
        with_gear_defense=role2.start_defense,
        with_gear_myst_attack=role2.start_myst_attack,
        with_gear_myst_defense=role2.start_myst_defense,
        with_gear_speed=role2.start_speed,
        ability_1=ability1,
        ability_2=ability6,
        ability_3=ability11,
        ability_4=ability16,
    )
    GameUser.objects.bulk_create(
        [
            gameuser1,
            gameuser2,
            gameuser3,
            gameuser4,
            gameuser5,
        ]
    )

    # npcs + images
    npc1 = NPC(name="Narrator", image="logo.png")
    npc2 = NPC(name="Old Man", image="old-man.png")
    npc3 = NPC(name="Drunk Man 1", image="drunk-man-1.png")
    npc4 = NPC(name="Drunk Man 2", image="drunk-man-2.png")
    NPC.objects.bulk_create(
        [
            npc1,
            npc2,
            npc3,
            npc4,
        ]
    )

    # Enemies
    enemy1 = Enemy(
        name="Drunk Man 1",
        image="drunk-man-1.png",
        type=type_light,
        start_hp=150,
        start_attack=50,
        start_defense=50,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability17,
        ability_2=ability17,
        ability_3=ability18,
        ability_4=ability19,
    )
    enemy2 = Enemy(
        name="Drunk Man 2",
        image="drunk-man-2.png",
        type=type_dark,
        start_hp=150,
        start_attack=50,
        start_defense=50,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability20,
        ability_2=ability20,
        ability_3=ability21,
        ability_4=ability22,
    )
    enemy3 = Enemy(
        name="Arachnid Sovereign",
        image="arachnid-sovereign.png",
        type=type_forest,
        start_hp=200,
        start_attack=60,
        start_defense=60,
        start_myst_attack=60,
        start_myst_defense=60,
        start_speed=60,
        ability_1=ability23,
        ability_2=ability23,
        ability_3=ability24,
        ability_4=ability25,
    )
    enemy4 = Enemy(
        name="Arachnid Minion",
        image="arachnid-minion.png",
        type=type_forest,
        start_hp=80,
        start_attack=40,
        start_defense=40,
        start_myst_attack=40,
        start_myst_defense=40,
        start_speed=75,
        ability_1=ability26,
        ability_2=ability26,
        ability_3=ability26,
        ability_4=ability26,
    )
    enemy5 = Enemy(
        name="Primordial Anomaly",
        image="primordial-anomaly.png",
        type=type_forest,
        start_hp=300,
        start_attack=100,
        start_defense=100,
        start_myst_attack=100,
        start_myst_defense=100,
        start_speed=100,
        ability_1=ability27,
        ability_2=ability28,
        ability_3=ability29,
        ability_4=ability30,
    )
    enemy6 = Enemy(
        name="Luminar Sentinel",
        image="luminar-sentinel.png",
        type=type_light,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=50,
        ability_1=ability31,
        ability_2=ability31,
        ability_3=ability32,
        ability_4=ability32,
    )
    enemy7 = Enemy(
        name="Umbral Harbinger",
        image="umbral-harbinger.png",
        type=type_dark,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=50,
        ability_1=ability33,
        ability_2=ability33,
        ability_3=ability34,
        ability_4=ability34,
    )
    enemy8 = Enemy(
        name="Granite Warden",
        image="granite-warden.png",
        type=type_stone,
        start_hp=100,
        start_attack=75,
        start_defense=75,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability35,
        ability_2=ability35,
        ability_3=ability36,
        ability_4=ability36,
    )
    enemy9 = Enemy(
        name="Sylvan Enchanter",
        image="sylvan-enchanter.png",
        type=type_forest,
        start_hp=100,
        start_attack=75,
        start_defense=75,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=75,
        ability_1=ability37,
        ability_2=ability37,
        ability_3=ability38,
        ability_4=ability38,
    )
    enemy10 = Enemy(
        name="Galewing Shaman",
        image="galewing-shaman.png",
        type=type_wind,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=75,
        ability_1=ability39,
        ability_2=ability39,
        ability_3=ability40,
        ability_4=ability40,
    )

    Enemy.objects.bulk_create(
        [
            enemy1,
            enemy2,
            enemy3,
            enemy4,
            enemy5,
            enemy6,
            enemy7,
            enemy8,
            enemy9,
            enemy10,
        ]
    )

    # Dialogue
    node1 = Dialogue(from_node_id=0, node_type="narration", speaker="Narrator",
                     text="Your group finds themselves teleported to an abandoned alleyway in what looks like a quaint old village. The narrow passage is dimly lit, and the silence is broken by the distant sounds of chatter and laughter. Suddenly, two drunk men spot your group and stagger towards you, their eyes gleaming with mischief.",
                     act=1, scene=1)
    node2 = Dialogue(from_node_id=1, node_type="talk", speaker="Drunk Man 1",
                     text="Blimey, would ya look at this lot! Fancied themselves lost tourists, do they?", act=1,
                     scene=1)
    node3 = Dialogue(from_node_id=2, node_type="talk", speaker="Drunk Man 2",
                     text="Aven't seen faces like these 'round 'ere before!", act=1, scene=1)
    node4 = Dialogue(from_node_id=3, node_type="talk", speaker="player1",
                     text="We don't mean any harm. We're just passing through, gentlemen.", act=1, scene=1)
    node5 = Dialogue(from_node_id=4, node_type="talk", speaker="Drunk Man 1",
                     text="Passin' through, eh? Not so fast! We don't get visitors often, so we might as well 'ave some fun with ya!",
                     act=1, scene=1)
    node6 = Dialogue(from_node_id=5, node_type="talk", speaker="player1",
                     text="We don't want any trouble. We'll be on our way.", act=1, scene=1)
    node7 = Dialogue(from_node_id=6, node_type="talk", speaker="Drunk Man 2", text="Not so fast! You're stayin' put!",
                     act=1, scene=1)
    node8 = Dialogue(from_node_id=7, node_type="talk", speaker="Old Man", text="Ey, what's all this ruckus?", act=1,
                     scene=1)
    node9 = Dialogue(from_node_id=8, node_type="talk", speaker="Drunk Man 1",
                     text="Stay out of this, old timer! These strangers are gonna get what's comin' to 'em!", act=1,
                     scene=1)
    node10 = Dialogue(from_node_id=9, node_type="talk", speaker="Old Man",
                      text="Now, now, lads. That's no way to treat our guests. Let 'em pass and be on their way.",
                      act=1, scene=1)
    node11 = Dialogue(from_node_id=10, node_type="talk", speaker="Drunk Man 2",
                      text="Fine, but they better not show their faces 'round here again!", act=1, scene=1)
    node12 = Dialogue(from_node_id=11, node_type="talk", speaker="Old Man",
                      text="I apologize for their behavior. They can get a bit rowdy when they've 'ad a few too many. Please, come inside my tavern. You'll be safe there.",
                      act=1, scene=1)
    node13 = Dialogue(from_node_id=12, node_type="talk", speaker="player1",
                      text="Thank you for your help. We'll gladly take shelter in your tavern.", act=1, scene=1)

    node14 = Dialogue(from_node_id=13, node_type="narration", speaker="Narrator",
                      text="As your group hurries into the tavern, the old man closes the door behind you, shutting out the noise and tension from the alleyway.",
                      act=1, scene=2)
    node15 = Dialogue(from_node_id=14, node_type="talk", speaker="Old Man",
                      text="Sit, sit! Let me tell ya a tale of our plight. Evil creatures, they are. Taking control over our town, the last stronghold of good in our world. We need help, you see, from individuals not easily swayed by these beasts. And, it dawns on me, I believe you and your group might be the ones we've been waitin' for.",
                      act=1, scene=2)
    node16 = Dialogue(from_node_id=15, node_type="talk", speaker="player1", text="Us? Why us?", act=1, scene=2)
    node17 = Dialogue(from_node_id=16, node_type="talk", speaker="Old Man",
                      text="Not entirely sure, my dear, but it seems fate has brought you here. We've been seekin' aid for a long time now, and you seem like a capable bunch. A band of mercenaries you ain't, but together, you make a good team.",
                      act=1, scene=2)
    node18 = Dialogue(from_node_id=17, node_type="talk", speaker="player1",
                      text="How did we even end up in this village?", act=1, scene=2)
    node19 = Dialogue(from_node_id=18, node_type="talk", speaker="Old Man",
                      text="Have another round, and I'll tell ya what I think. As for the \"how\"... well, we're in a magical and mysterious place, ain't we? My guess is that you were brought here for a reason. The only way to defeat these creatures is with outside help, and you seem like the help we need.",
                      act=1, scene=2)
    node20 = Dialogue(from_node_id=19, node_type="talk", speaker="player1",
                      text="Why now? Why did we end up here at this specific time?", act=1, scene=2)
    node21 = Dialogue(from_node_id=20, node_type="talk", speaker="Old Man",
                      text="Time's runnin' out, I'm afraid. These creatures are changin', and it's not for the better. Other towns nearby have already felt their wrath. We're on the brink of losin' ourselves. You might just be our last hope.",
                      act=1, scene=2)
    node22 = Dialogue(from_node_id=21, node_type="talk", speaker="player1",
                      text="But we're not warriors or fighters. We're just regular old people!", act=1, scene=2)
    node23 = Dialogue(from_node_id=22, node_type="talk", speaker="Old Man",
                      text="Regular people, eh? I don't believe that for a second. I believe you have somethin' within you. You'll find what you need to face this challenge. First things first, get a room upstairs in the tavern inn. In the morning, head to the general store and gather some equipment for your journey. You'll need it before you set off.",
                      act=1, scene=2)
    node24 = Dialogue(from_node_id=23, node_type="choice", speaker="player1",
                      text="1. Book a night at the inn and see what tomorrow brings.", act=1, scene=2)
    node25 = Dialogue(from_node_id=23, node_type="choice", speaker="player1",
                      text="2. Attempt to leave the tavern and try to get home.", act=1, scene=2)
    node26 = Dialogue(from_node_id=23, node_type="choice", speaker="player1",
                      text="3. Continue to talk to the old man.", act=1, scene=2)

    node27 = Dialogue(from_node_id=24, node_type="talk", speaker="player1",
                      text="We've had quite a day. Maybe we should get some rest, see what tomorrow brings.", act=1,
                      scene=3)
    node28 = Dialogue(from_node_id=27, node_type="talk", speaker="player2",
                      text="It's been a lot to take in. A good night's rest might clear our heads.", act=1, scene=3)
    node29 = Dialogue(from_node_id=28, node_type="talk", speaker="player3",
                      text="But what if we're really stuck here? We can't just wait around forever.", act=1, scene=3)
    node30 = Dialogue(from_node_id=29, node_type="talk", speaker="player1",
                      text="We'll keep our eyes and ears open. If there's a chance to find our way back, we'll take it. For now, let's book a night at the inn and regroup in the morning.",
                      act=1, scene=3)
    node31 = Dialogue(from_node_id=30, node_type="narration", speaker="Narrator",
                      text="As the group gets settled into their room above the tavern inn, they realize they have a window with a view into the very same alleyway they found themselves in earlier that evening.",
                      act=1, scene=3)
    node32 = Dialogue(from_node_id=31, node_type="talk", speaker="player2",
                      text="Hold on, everyone. Come take a look at this!", act=1, scene=3)
    node33 = Dialogue(from_node_id=32, node_type="talk", speaker="player3", text="What is it?", act=1, scene=3)
    node34 = Dialogue(from_node_id=33, node_type="talk", speaker="player2",
                      text="It's the exact spot where we found ourselves transported! There's a weird glimmer in the air. I think we should investigate.",
                      act=1, scene=3)
    node35 = Dialogue(from_node_id=34, node_type="talk", speaker="player1",
                      text="You're right. It's worth checking out. Let's head over there and see if we can find any clues.",
                      act=1, scene=3)

    node36 = Dialogue(from_node_id=25, node_type="talk", speaker="player2",
                      text="We can't just sit around here hoping for answers. We need to go back to where we entered this place and look for clues. Maybe we'll find a way back home.",
                      act=1, scene=4)
    node37 = Dialogue(from_node_id=36, node_type="talk", speaker="player3",
                      text="I agree. It's worth a shot. We should at least try to retrace our steps.", act=1, scene=4)
    node38 = Dialogue(from_node_id=37, node_type="talk", speaker="player1",
                      text="Alright, it's settled then. Let's head back to the alley and see if we can find any clues.",
                      act=1, scene=4)

    node39 = Dialogue(from_node_id=26, node_type="narration", speaker="Narrator",
                      text="The group debates their options, torn between waiting for answers and seeking a way back home. They turn back to the old man and he is passed out under the table.",
                      act=1, scene=5)
    node40 = Dialogue(from_node_id=39, node_type="talk", speaker="player2",
                      text="I think he's had a bit too much to drink. Maybe we should leave him be for now.", act=1,
                      scene=5)
    node41 = Dialogue(from_node_id=40, node_type="talk", speaker="player1",
                      text="Agreed. Let's try to figure this out on our own for now.", act=1, scene=5)

    node101 = Dialogue(from_node_id=100, node_type="talk", speaker="player1",
                       text="Do you guys feel that too? It's like there's something... different.", act=1, scene=6)
    node102 = Dialogue(from_node_id=101, node_type="talk", speaker="player2",
                       text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=6)
    node103 = Dialogue(from_node_id=102, node_type="talk", speaker="player3",
                       text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=6)
    node104 = Dialogue(from_node_id=103, node_type="talk", speaker="Drunk Man 1",
                       text="Look who's back for another beating!", act=1, scene=6)
    node105 = Dialogue(from_node_id=104, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!",
                       act=1, scene=6)
    node106 = Dialogue(from_node_id=105, node_type="talk", speaker="player1",
                       text="We've had enough of this. Let's just take these guys out.", act=1, scene=6)

    node107 = Dialogue(from_node_id=106, node_type="narration", speaker="Narrator", text="{battle 1 outcome}", act=1,
                       scene=7)
    node108 = Dialogue(from_node_id=107, node_type="talk", speaker="Old Man",
                       text="What in blazes were ya thinkin', runnin' off like that? I told you the town was slowly descending into chaos and your response to that was to go out into the unknown?! Idiots!",
                       act=1, scene=7)
    node109 = Dialogue(from_node_id=108, node_type="talk", speaker="player1",
                       text="We didn't mean to cause any trouble. We just thought we could handle it.", act=1, scene=7)
    node110 = Dialogue(from_node_id=109, node_type="talk", speaker="Old Man",
                       text="Handle it, eh? You young ones are too green to be takin' on those ruffians. Now, let's get you all up to your room.",
                       act=1, scene=7)

    node111 = Dialogue(from_node_id=110, node_type="talk", speaker="Old Man",
                       text="Be ready to head to the store in the mornin'. You'll need supplies if you're plannin' to stay and help us. After that, I will teach you to fight. Goodnight!",
                       act=1, scene=8)
    node112 = Dialogue(from_node_id=111, node_type="narration", speaker="Narrator",
                       text="The old man promptly sits in the chair and immediately falls asleep.", act=1, scene=8)
    node113 = Dialogue(from_node_id=112, node_type="talk", speaker="player1",
                       text="Well, that was unexpected. Maybe we should have one person awake on lookout. Who knows what's out there.",
                       act=1, scene=8)
    node114 = Dialogue(from_node_id=113, node_type="talk", speaker="player2", text="I'll take the first watch.", act=1,
                       scene=8)

    node115 = Dialogue(from_node_id=114, node_type="narration", speaker="Narrator",
                       text="The group wakes up in their room, feeling refreshed after a night of rest, only to be greeted by the old man poking them with his cane.",
                       act=1, scene=9)
    node116 = Dialogue(from_node_id=115, node_type="talk", speaker="Old Man",
                       text="Rise and shine, sleepyheads! Time's a-wastin', and there's much to be done!", act=1,
                       scene=9)
    node117 = Dialogue(from_node_id=116, node_type="talk", speaker="player1",
                       text="Good morning to you too, but do you have to be so loud?", act=1, scene=9)
    node118 = Dialogue(from_node_id=117, node_type="talk", speaker="Old Man",
                       text="Loud is the only way to get you young ones movin'! Now, listen up! Sleep is very important here. Very restorative, yes, especially for warriors such as yourselves. You must be available for battle at all times.",
                       act=1, scene=9)
    node119 = Dialogue(from_node_id=118, node_type="talk", speaker="player2",
                       text="We're not warriors. How many times do we have to tell you?", act=1, scene=9)
    node120 = Dialogue(from_node_id=119, node_type="talk", speaker="Old Man",
                       text="That may be so, but you're our best chance at pushin' back those nasty creatures. You've got potential, and with a good night's sleep, you'll be even better prepared for what lies ahead.",
                       act=1, scene=9)
    node121 = Dialogue(from_node_id=120, node_type="talk", speaker="player3",
                       text="How do you know so much about this place and the creatures? Have you been fighting them for long?",
                       act=1, scene=9)
    node122 = Dialogue(from_node_id=121, node_type="talk", speaker="Old Man",
                       text="Aye, I've seen my fair share of battles in this village. Been fightin' these beasts for longer than I care to remember. But I'm gettin' too old for this now. That's why we need you young ones.",
                       act=1, scene=9)
    node123 = Dialogue(from_node_id=122, node_type="talk", speaker="player4",
                       text="We just got wasted by two drunk guys last night. How do you expect us to help?", act=1,
                       scene=9)
    node124 = Dialogue(from_node_id=123, node_type="talk", speaker="Old Man",
                       text="Aye, that's the spirit! We'll head to my house and get what you need.", act=1, scene=9)
    node125 = Dialogue(from_node_id=124, node_type="narration", speaker="Narrator",
                       text="The group looks at each other, stunned, not sure what to do. The old man doesn't even seem to be listening to them. They begrugingly agree to follow the old man to his house, hoping to get a glimpse of the spot they appeared at the night before.",
                       act=1, scene=9)

    node126 = Dialogue(from_node_id=125, node_type="talk", speaker="Old Man",
                       text="Wait here and I'll go in and scrounge up some stuffs for ya.", act=1, scene=10)
    node127 = Dialogue(from_node_id=126, node_type="talk", speaker="player4",
                       text="What the heck is going on. Are we really doing this?", act=1, scene=10)
    node128 = Dialogue(from_node_id=127, node_type="talk", speaker="player3", text="Got any other ideas?", act=1,
                       scene=10)
    node129 = Dialogue(from_node_id=128, node_type="narration", speaker="Narrator",
                       text="The old man reappears with a bunch of raggedy clothes and what look to be wooden weapons.",
                       act=1, scene=10)
    node130 = Dialogue(from_node_id=129, node_type="talk", speaker="Old Man",
                       text="Well this will have to do for now... Whittled by meself these!", act=1, scene=10)
    node131 = Dialogue(from_node_id=130, node_type="talk", speaker="Old Man",
                       text="First, for {player1}. I give to you my {weapon1} and {armor1}. You are a {role}. {short_role_summary}. I beg of you, save us.",
                       act=1, scene=10)
    node132 = Dialogue(from_node_id=131, node_type="narration", speaker="Narrator",
                       text="{player1} has learned {ability2}!", act=1, scene=10)
    node133 = Dialogue(from_node_id=132, node_type="talk", speaker="Old Man",
                       text="Second, for {player2}. I give to you my {weapon1} and {armor1}. You are a {role}. {short_role_summary}. I beg of you, save us.",
                       act=1, scene=10)
    node134 = Dialogue(from_node_id=133, node_type="narration", speaker="Narrator",
                       text="{player2} has learned {ability2}!", act=1, scene=10)
    node135 = Dialogue(from_node_id=134, node_type="talk", speaker="Old Man",
                       text="Third, for {player3}. I give to you my {weapon1} and {armor1}. You are a {role}. {short_role_summary}. I beg of you, save us.",
                       act=1, scene=10)
    node136 = Dialogue(from_node_id=135, node_type="narration", speaker="Narrator",
                       text="{player3} has learned {ability2}!", act=1, scene=10)
    node137 = Dialogue(from_node_id=136, node_type="talk", speaker="Old Man",
                       text="Fourth, for {player4}. I give to you my {weapon1} and {armor1}. You are a {role}. {short_role_summary}. The fate of our world lies in your hands. I beg of you, save us.",
                       act=1, scene=10)
    node138 = Dialogue(from_node_id=137, node_type="narration", speaker="Narrator",
                       text="{player4} has learned {ability2}!", act=1, scene=10)

    node139 = Dialogue(from_node_id=138, node_type="narration", speaker="Narrator",
                       text="The old man walks past them without another word hobbling to the edge of town. A silence came upon the group. The group hurries to put their new weapons and armor on and follow him.",
                       act=1, scene=11)
    node140 = Dialogue(from_node_id=139, node_type="talk", speaker="Old Man",
                       text="May these weapons and armor embolden you. Now I reckon when you left the tavern last night you felt something was different. A feeling in the back of your mind that wasn't there before. This is called Mystic Power. This power, everyone has, but few know how to wield it. Keep it in your thoughts. Practice it, harness it. Use it to defeat evil. There is truly something mystical about this tavern. It has a way of opening peoples' awareness to their inner power.",
                       act=1, scene=11)
    node141 = Dialogue(from_node_id=140, node_type="talk", speaker="Old Man",
                       text="The greater the strength of the ability you use, the more Mystic Power will be needed for it. Use it with caution for this power is not unlimited, and must be replenished through rest.",
                       act=1, scene=11)
    node142 = Dialogue(from_node_id=141, node_type="talk", speaker="Old Man",
                       text="When I gave you your equipment I could sense that each of you awakened a new ability within yourselves. As you may have noticed in your scuffle last night, your fists do very little here. A touch of Mystic Power is necessary to overpower your opponents. Don't worry. You will learn more abilities as you progress on your travels.",
                       act=1, scene=11)
    node143 = Dialogue(from_node_id=142, node_type="talk", speaker="Old Man", text="I leave you he----", act=1,
                       scene=11)
    node144 = Dialogue(from_node_id=143, node_type="talk", speaker="Drunk Man 1",
                       text="There they are! Back for more are ya?!", act=1, scene=11)

    node145 = Dialogue(from_node_id=144, node_type="narration", speaker="Narrator",
                       text="You wake up to the old man giving your group an elixer", act=1, scene=12)
    node146 = Dialogue(from_node_id=145, node_type="talk", speaker="Old Man",
                       text="Wakey wakey. This isn't gonna be no cakewalk. Maybe you aren't cut out for this.. Shame. Not sure anyone else is left.",
                       act=1, scene=12)
    node147 = Dialogue(from_node_id=146, node_type="talk", speaker="player1",
                       text="No. We can do this. We were much better this time. We just need to practice.", act=1,
                       scene=12)
    node148 = Dialogue(from_node_id=147, node_type="talk", speaker="Old Man",
                       text="Your spirit is encouraging. Unfortunately, you will have to learn by doing, but I should be able to get some extra equipment for you all before we leave. My whittlework and old rags don't seem to be cutting it. Time is of the essense. Let me take you to the edge of town.",
                       act=1, scene=12)

    node149 = Dialogue(from_node_id=144, node_type="talk", speaker="Old Man",
                       text="Well well well, congratulations. It looks like you will do just fine out there. Those guys are pretty tough.",
                       act=1, scene=13)
    node150 = Dialogue(from_node_id=149, node_type="talk", speaker="player1", text="Great work team!", act=1, scene=13)
    node151 = Dialogue(from_node_id=150, node_type="talk", speaker="player2", text="Just kickin' ass and takin' names.",
                       act=1, scene=13)
    node152 = Dialogue(from_node_id=151, node_type="talk", speaker="Old Man",
                       text="Your spirit is encouraging. Get some gold off those guys, then follow me! Time is of the essense. Let me take you to the edge of town.",
                       act=1, scene=13)
    node153 = Dialogue(from_node_id=152, node_type="narration", speaker="Narrator",
                       text="{player1} has received 5 gold!", act=1, scene=13)
    node154 = Dialogue(from_node_id=153, node_type="narration", speaker="Narrator",
                       text="{player2} has received 5 gold!", act=1, scene=13)
    node155 = Dialogue(from_node_id=154, node_type="narration", speaker="Narrator",
                       text="{player3} has received 5 gold!", act=1, scene=13)
    node156 = Dialogue(from_node_id=155, node_type="narration", speaker="Narrator",
                       text="{player4} has received 5 gold!", act=1, scene=13)

    node157 = Dialogue(from_node_id=144, node_type="talk", speaker="Old Man",
                       text="Well well well, congratulations. It looks like you will do just fine out there. Those guys are pretty tough. A bit worse for wear, but nothing my special elixer can't fix. Here you go.",
                       act=1, scene=14)
    node158 = Dialogue(from_node_id=157, node_type="talk", speaker="player1", text="Great work team!", act=1, scene=14)
    node159 = Dialogue(from_node_id=158, node_type="talk", speaker="player2", text="Just kickin' ass and takin' names",
                       act=1, scene=14)
    node160 = Dialogue(from_node_id=159, node_type="talk", speaker="Old Man",
                       text="Your spirit is encouraging. Get some gold off those guys, then follow me! Time is of the essense. Let me take you to the edge of town.",
                       act=1, scene=14)
    node161 = Dialogue(from_node_id=160, node_type="narration", speaker="Narrator",
                       text="{player1} has received 5 gold!", act=1, scene=14)
    node162 = Dialogue(from_node_id=161, node_type="narration", speaker="Narrator",
                       text="{player2} has received 5 gold!", act=1, scene=14)
    node163 = Dialogue(from_node_id=162, node_type="narration", speaker="Narrator",
                       text="{player3} has received 5 gold!", act=1, scene=14)
    node164 = Dialogue(from_node_id=163, node_type="narration", speaker="Narrator",
                       text="{player4} has received 5 gold!", act=1, scene=14)

    node201 = Dialogue(from_node_id=200, node_type="talk", speaker="Old Man",
                       text="I don't want to understate our dire situation. You may very well be our last hope.", act=1,
                       scene=15)
    node202 = Dialogue(from_node_id=201, node_type="talk", speaker="Old Man",
                       text="Remember these things: Communicate with your group! Make sure everyone agrees on the decision, trust each other. Unfortunately, trust nearly no one else. You are entering into the unknown out there. Nobody who has left has come back. Get rest as much as possible. Train as much as you can, get better equipment any way you can. As far as I know, the creature.. or creatures... doing this to us is down this road. It's your decision alone on what to do from there. Trust your instincts. Good luck.",
                       act=1, scene=15)
    node203 = Dialogue(from_node_id=202, node_type="narration", speaker="Narrator",
                       text="The group stares out down the road.", act=1, scene=15)
    node204 = Dialogue(from_node_id=203, node_type="talk", speaker="player4",
                       text="Your directions are just down the road? Surely you have more to go on than -----", act=1,
                       scene=15)
    node205 = Dialogue(from_node_id=204, node_type="narration", speaker="Narrator",
                       text="The group turns around and the old man has vanished.", act=1, scene=15)
    node206 = Dialogue(from_node_id=205, node_type="talk", speaker="player3", text="Great.", act=1, scene=15)
    node207 = Dialogue(from_node_id=206, node_type="talk", speaker="player2",
                       text="Well... onward and upward, I guess.", act=1, scene=15)
    node208 = Dialogue(from_node_id=207, node_type="narration", speaker="Narrator",
                       text="{player1} kneels down next to where the old man was standing and rises up, fists closed.",
                       act=1, scene=15)
    node209 = Dialogue(from_node_id=208, node_type="talk", speaker="player4",
                       text="What's that you got there? Did he drop something?", act=1, scene=15)
    node210 = Dialogue(from_node_id=209, node_type="narration", speaker="Narrator",
                       text="{player1} extends his palms out to the group revealing five crystals, one white, one black, one green, one grey, one purple.",
                       act=1, scene=15)
    node211 = Dialogue(from_node_id=210, node_type="narration", speaker="Narrator",
                       text="{player1} kneels down, digs a small hole, and places the green crystal in it and fills the hole back in, puts his hand on the agitated dirt and mutters something. The ground lights up green for a few seconds then dies away.",
                       act=1, scene=15)
    node212 = Dialogue(from_node_id=211, node_type="talk", speaker="player3", text="What did you just do?", act=1,
                       scene=15)
    node213 = Dialogue(from_node_id=212, node_type="talk", speaker="player1",
                       text="I... I don't know... but it felt like the correct thing to do. Looks like there's one for each of us. Take one for yourselves and let's head out.",
                       act=1, scene=15)
    node214 = Dialogue(from_node_id=213, node_type="narration", speaker="Narrator",
                       text="{player1} takes the white crystal, {player2} takes the black crystal, {player3} takes the grey crystal, and {player4} takes the purple crystal.",
                       act=1, scene=15)

    Dialogue.objects.bulk_create(
        [
            node1, node2, node3, node4, node5, node6, node7, node8, node9, node10, node11, node12, node13,
            node14, node15, node16, node17, node18, node19, node20, node21, node22, node23, node24, node25, node26,
            node27, node28, node29, node30, node31, node32, node33, node34, node35,
            node36, node37, node38,
            node39, node40, node41,
            node101, node102, node103, node104, node105, node106,
            node107, node108, node109, node110,
            node111, node112, node113, node114,
            node115, node116, node117, node118, node119, node120, node121, node122, node123, node124, node125,
            node126, node127, node128, node129, node130, node131, node132, node133, node134, node135, node136, node137, node138,
            node139, node140, node141, node142, node143, node144,
            node145, node146, node147, node148,
            node149, node150, node151, node152, node153, node154, node155, node156,
            node157, node158, node159, node160, node161, node162, node163, node164,
            node201, node202, node203, node204, node205, node206, node207, node208, node209, node210, node211, node212, node213, node214,
        ]
    )
