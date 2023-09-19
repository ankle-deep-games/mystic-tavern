from ..models import Game, GameUser, Role, Gender, Dialogue, NPC, Type, Weapon, Armor, Ability, Enemy
from django.contrib.auth.models import User

def seed_data():
    # users are special because they get created with a hashed password with create_user
    user1 = User.objects.create_user(username='john', email='jlennon@beatles.com', password='imagine')
    user2 = User.objects.create_user(username='paul', email='pmccartney@beatles.com', password='let it be')
    user3 = User.objects.create_user(username='george', email='gharrison@beatles.com',password='my sweet lord')
    user4 = User.objects.create_user(username='ringo', email='rstarr@beatles.com', password='yellow submarine')
    user5 = User.objects.create_user(username='eleanor', email='erigby@beatles.com', password='lonely people')
    user1.save()
    user2.save()
    user3.save()
    user4.save()
    user5.save()

    # games
    game1 = Game(name="Game Seed 1", creator=user1, game_started=False, game_over=False, password="apple")
    game2 = Game(name="Game Seed 2", creator=user2, game_started=False, game_over=False, password="banana")
    Game.objects.bulk_create([
        game1,
        game2,
    ])

    # types
    type1 = Type(name="Light", strength=2, weakness=5)
    type2 = Type(name="Dark", strength=3, weakness=1)
    type3 = Type(name="Stone", strength=4, weakness=2)
    type4 = Type(name="Forest", strength=5, weakness=3)
    type5 = Type(name="Wind", strength=1, weakness=4)
    type6 = Type(name="Normal", strength=6, weakness=6)
    Type.objects.bulk_create([
        type1,
        type2,
        type3,
        type4,
        type5,
        type6,
    ])

    # roles
    role1 = Role(name="WHITEMAGE", type=type1, start_hp=100, start_mp=100, start_attack=10, start_defense=20, start_myst_attack=15, start_myst_defense=20, start_speed=25)
    role2 = Role(name="BLACKMAGE", type=type2, start_hp=80, start_mp=120, start_attack=15, start_defense=10, start_myst_attack=35, start_myst_defense=10, start_speed=30)
    role3 = Role(name="PALADIN", type=type3, start_hp=120, start_mp=80, start_attack=20, start_defense=30, start_myst_attack=10, start_myst_defense=20, start_speed=20)
    role4 = Role(name="ARCHER", type=type4, start_hp=110, start_mp=90, start_attack=35, start_defense=15, start_myst_attack=10, start_myst_defense=10, start_speed=30)
    role5 = Role(name="BARD", type=type5, start_hp=90, start_mp=110, start_attack=20, start_defense=20, start_myst_attack=20, start_myst_defense=20, start_speed=20)
    Role.objects.bulk_create([
        role1,
        role2,
        role3,
        role4,
        role5,
    ])

    # genders
    gender1 = Gender(name="MALE")
    gender2 = Gender(name="FEMALE")
    Gender.objects.bulk_create([
        gender1,
        gender2,
    ])

    # weapons
    weapon1 = Weapon(name="Wood Staff", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon2 = Weapon(name="Wood Sword", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon3 = Weapon(name="Wood Bow", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon4 = Weapon(name="Wood Flute", attack_mod=5, myst_attack_mod=5, speed_mod=5, mp_mod=5)
    weapon5 = Weapon(name="Longsword", attack_mod=26, myst_attack_mod=12, speed_mod=10, mp_mod=12)
    weapon6 = Weapon(name="Longbow", attack_mod=26, myst_attack_mod=10, speed_mod=12, mp_mod=12)
    weapon7 = Weapon(name="Ivory Rod", attack_mod=10, myst_attack_mod=20, speed_mod=10, mp_mod=20)
    weapon8 = Weapon(name="Obsidian Wand", attack_mod=10, myst_attack_mod=22, speed_mod=10, mp_mod=18)
    weapon9 = Weapon(name="Melodious Lute", attack_mod=10, myst_attack_mod=20, speed_mod=12, mp_mod=18)
    weapon10 = Weapon(name="Holy Avenger", attack_mod=30, myst_attack_mod=25, speed_mod=15, mp_mod=20)
    weapon11 = Weapon(name="Shadowstrike", attack_mod=35, myst_attack_mod=15, speed_mod=20, mp_mod=20)
    weapon12 = Weapon(name="Divine Scepter", attack_mod=15, myst_attack_mod=30, speed_mod=15, mp_mod=30)
    weapon13 = Weapon(name="Voidcaller", attack_mod=15, myst_attack_mod=30, speed_mod=15, mp_mod=30)
    weapon14 = Weapon(name="Symphony Harp", attack_mod=15, myst_attack_mod=30, speed_mod=17, mp_mod=28)
    weapon15 = Weapon(name="Excalibur", attack_mod=45, myst_attack_mod=30, speed_mod=20, mp_mod=25)
    weapon16 = Weapon(name="Arbalest", attack_mod=53, myst_attack_mod=20, speed_mod=22, mp_mod=25)
    weapon17 = Weapon(name="Seraph's Wand", attack_mod=20, myst_attack_mod=40, speed_mod=20, mp_mod=40)
    weapon18 = Weapon(name="Ulrich Tome", attack_mod=20, myst_attack_mod=40, speed_mod=20, mp_mod=40)
    weapon19 = Weapon(name="Seranade Baton", attack_mod=20, myst_attack_mod=38, speed_mod=22, mp_mod=40)
    Weapon.objects.bulk_create([
        weapon1,
        weapon2,
        weapon3,
        weapon4,
        weapon5,
        weapon6,
        weapon7,
        weapon8,
        weapon9,
        weapon10,
        weapon11,
        weapon12,
        weapon13,
        weapon14,
        weapon15,
        weapon16,
        weapon17,
        weapon18,
        weapon19,
    ])

    # armor
    armor1 = Armor(name="Cloth Tunic", defense_mod=5, myst_defense_mod=5, speed_mod=5, hp_mod=5, mp_mod=5)
    armor2 = Armor(name="Steel Plate Armor", defense_mod=20, myst_defense_mod=20, speed_mod=10, hp_mod=15, mp_mod=10)
    armor3 = Armor(name="Leather Armor", defense_mod=15, myst_defense_mod=15, speed_mod=15, hp_mod=15, mp_mod=15)
    armor4 = Armor(name="Acolyte's Robes", defense_mod=18, myst_defense_mod=20, speed_mod=10, hp_mod=12, mp_mod=15)
    armor5 = Armor(name="Sorcerer's Robes", defense_mod=10, myst_defense_mod=20, speed_mod=15, hp_mod=10, mp_mod=20)
    armor6 = Armor(name="Harmonist's Cummerbund", defense_mod=10, myst_defense_mod=20, speed_mod=15, hp_mod=10, mp_mod=20)
    armor7 = Armor(name="Radiant Valor Plate", defense_mod=20, myst_defense_mod=25, speed_mod=15, hp_mod=30, mp_mod=23)
    armor8 = Armor(name="Elven Windwrap", defense_mod=20, myst_defense_mod=20, speed_mod=30, hp_mod=25, mp_mod=18)
    armor9 = Armor(name="Archmage's Vestments", defense_mod=25, myst_defense_mod=18, speed_mod=20, hp_mod=25, mp_mod=25)
    armor10 = Armor(name="Warlock's Cloak", defense_mod=25, myst_defense_mod=20, speed_mod=20, hp_mod=20, mp_mod=28)
    armor11 = Armor(name="Virtuoso's Ensemble", defense_mod=25, myst_defense_mod=20, speed_mod=23, hp_mod=20, mp_mod=25)
    armor12 = Armor(name="Divine Warplate", defense_mod=40, myst_defense_mod=40, speed_mod=20, hp_mod=30, mp_mod=20)
    armor13 = Armor(name="Galestrider Vest", defense_mod=35, myst_defense_mod=35, speed_mod=35, hp_mod=25, mp_mod=20)
    armor14 = Armor(name="Celestrial Regalia", defense_mod=25, myst_defense_mod=40, speed_mod=30, hp_mod=25, mp_mod=30)
    armor15 = Armor(name="Shadowweave Cape", defense_mod=20, myst_defense_mod=40, speed_mod=35, hp_mod=20, mp_mod=35)
    armor16 = Armor(name="Maestro's Tailcoat", defense_mod=20, myst_defense_mod=40, speed_mod=35, hp_mod=20, mp_mod=35)
    Armor.objects.bulk_create([
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
        armor12,
        armor13,
        armor14,
        armor15,
        armor16,
    ])

    # abilities
    # Tier 1
    ability1 = Ability(name="Attack",
                       description="A basic single-target physical attack that inflicts low damage without consuming MP.",
                       type=type6, mp_cost=0, is_myst_attack=False, is_heal=False, is_aoe=False, is_buff=False, min_damage=1, max_damage=5)
    # Tier 2
    ability2 = Ability(name="Shield Bash",
                       description="A physical attack that deals low damage to one enemy by thrusting a shield into the enemy.",
                       type=type3, mp_cost=5, is_myst_attack=False, is_heal=False, is_aoe=False, is_buff=False, min_damage=5, max_damage=15)
    ability3 = Ability(name="Shatter Shot",
                       description="A precise single-target physical attack that delivers medium damage to one enemy with a precisely aimed arrow.",
                       type=type4, mp_cost=5, is_myst_attack=False, is_heal=False, is_aoe=False, is_buff=False, min_damage=5, max_damage=15)
    ability4 = Ability(name="Divine Light",
                       description="A single-target healing spell that provides a gentle, low-level healing effect to one ally with a radiant burst of light.",
                       type=type1, mp_cost=10, is_myst_attack=True, is_heal=True, is_aoe=False, is_buff=False, min_damage=5, max_damage=15)
    ability5 = Ability(name="Shadow Blast",
                       description="A focused single-target attack that inflicts medium damage on one enemy through a powerful surge of arcane energy.",
                       type=type2, mp_cost=10, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=5, max_damage=15)
    # TODO https://trello.com/c/BKxfLrtR/218-combat-buffs-add-update-seed-data
    ability6 = Ability(name="Anthem of Valor",
                       description="Empowers a single ally with a medium physical attack boost and a defensive buff, enhancing their strength and resilience.",
                       type=type5, mp_cost=10, is_myst_attack=False, is_heal=False,
                       is_aoe=False, is_buff=True, buff_attack_percent=0.1, buff_defense_percent=0.1)
    # Tier 3 - Light
    ability7 = Ability(name="Divine Strike",
                       description="Launches a medium mystic attack, harnessing the power of light to strike a single target with celestial force.",
                       type=type1, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability8 = Ability(name="Nature's Embrace",
                       description="Invokes the light of the natural world to deliver a medium mystic attack, enveloping a single target in the gentle yet powerful embrace of nature's energy.",
                       type=type1, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability9 = Ability(name="Radiant Surge",
                       description="Casts forth a medium mystic attack that surges with blinding light, striking a single target with intense brilliance and energy.",
                       type=type1, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability10 = Ability(name="Luminous Sonata",
                        description="Creates a harmoneous performance that conjures a medium mystic attack that envelopes a single target in a symphony of luminescent power.",
                        type=type1, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    # Tier 3 - Dark
    ability11 = Ability(name="Shadow Strike",
                       description="Unleashes a medium mystic attack with dark energy, striking a single target with shadowy force.",
                       type=type2, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability12 = Ability(name="Shadow Volley",
                       description="Fires a barrage of dark-infused arrows in a medium mystic attack that targets a single enemy.",
                       type=type2, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability13 = Ability(name="Dark Embrace",
                       description="Bestows a medium mystic attack infused with dark power upon a single target, enshrouding them in malevolent energy.",
                       type=type2, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability14 = Ability(name="Ebon Serenade",
                        description="Performs a haunting serenade to conjure a medium mystic attack, enveloping a single target in a melody of darkness.",
                        type=type2, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    # Tier 3 - Forest
    ability15 = Ability(name="Timber Slam",
                       description="Delivers a medium mystic attack imbued with the essence of the forest, striking a single target with the force of nature.",
                       type=type4, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability16 = Ability(name="Thorned Grasp",
                       description="Casts a medium mystic attack infused with the untamed power of the forest, enveloping a single target in thorny vines and natural wrath.",
                       type=type4, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability17 = Ability(name="Sylvan Whispers",
                       description="Unleashes a medium mystic attack that channels the secrets of the forest, enveloping a single target in whispers of natural power.",
                       type=type4, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability18 = Ability(name="Enchanted Grove",
                        description="Evokes the magic of the forest with a medium mystic attack, creating an enchanting grove that envelops a single target.",
                        type=type4, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    # Tier 3 - Stone
    ability19 = Ability(name="Piercing Arrow",
                       description="Fires a precise medium mystic attack in the form of a piercing arrow, targeting a single enemy.",
                       type=type3, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability20 = Ability(name="Stoneguard",
                       description="Conjures a medium mystic attack that fractures the very earth, targeting a single enemy with a devastating quake of stone and debris.",
                       type=type3, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability21 = Ability(name="Petrifying Blast",
                       description="Unleashes a medium mystic attack that carries the power to petrify, encasing a single target in stone-like rigidity.",
                       type=type3, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability22 = Ability(name="Resonant Stones",
                        description="Conjures a medium mystic attack with resonating stones, creating a harmonious symphony that engulfs a single target.",
                        type=type3, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    # Tier 3 - Wind
    ability23 = Ability(name="Cyclone Slash",
                       description="Executes a medium mystic attack, wielding the power of the wind to unleash a cyclonic strike upon a single target.",
                       type=type5, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability24 = Ability(name="Storm of Arrows",
                       description="Unleashes a tempestuous barrage of arrows in a medium mystic attack, targeting a single enemy.",
                       type=type5, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability25 = Ability(name="Gale Fury",
                       description="Commands a medium mystic attack imbued with the tempest's might, releasing a raging windstorm upon a single target, inflicting swirling damage.",
                       type=type5, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    ability26 = Ability(name="Tempest Nova",
                        description="Casts forth a medium mystic attack that erupts with the fury of a tempest, striking a single target with turbulent force.",
                        type=type5, mp_cost=20, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=15, max_damage=30)
    # Tier 4
    ability27 = Ability(name="Holy Wrath",
                       description="Summons divine fury, delivering a devastating high physical attack that channels holy energy to smite a single target with righteous force.",
                       type=type3, mp_cost=30, is_myst_attack=False, is_heal=False, is_aoe=False, is_buff=False, min_damage=30, max_damage=45)
    ability28 = Ability(name="Grove's Vengeance",
                       description="Harnesses the fury of the forest, unleashing a potent high physical attack that embodies the wrath of nature upon a single target.",
                       type=type4, mp_cost=30, is_myst_attack=False, is_heal=False, is_aoe=False, is_buff=False, min_damage=30, max_damage=45)
    ability29 = Ability(name="Sanctuary",
                       description="Invokes a healing haven, granting a substantial high-level heal that envelops a single target in a protective aura of rejuvenation.",
                       type=type1, mp_cost=30, is_myst_attack=True, is_heal=True, is_aoe=False, is_buff=False, min_damage=30, max_damage=45)
    ability30 = Ability(name="Arcane Darkness",
                        description="Conjures dark mystic forces, casting a formidable high mystic attack that shrouds a single target in shadowy, unpredictable energies.",
                        type=type2, mp_cost=30, is_myst_attack=True, is_heal=False, is_aoe=False, is_buff=False, min_damage=30, max_damage=45)
    # TODO https://trello.com/c/BKxfLrtR/218-combat-buffs-add-update-seed-data
    ability31 = Ability(name="Ethereal Crescendo",
                        description="Orchestrates a symphony of power, bestowing a robust buff to all stats upon a single target, elevating them to an ethereal peak of strength and grace.",
                        type=type5, mp_cost=30, is_myst_attack=False, is_heal=False,
                        is_aoe=True, is_buff=True, buff_hp_percent=0.5, buff_mp_percent=0.5, buff_attack_percent=0.5, buff_defense_percent=0.5, buff_myst_attack_percent=0.5, buff_myst_defense_percent=0.5, buff_speed_percent=0.5)
    
    # AOE test abilities TODO https://trello.com/c/jYTBJRi6/210-combat-aoe-add-update-aoe-abilities-in-abilities-seed-data
    ability32 = Ability(name="AOE Damage",
                       description="AOE Damage Test. Used by both players and enemies.",
                       type=type4, mp_cost=5, is_myst_attack=False, is_heal=False, is_aoe=True, is_buff=False, min_damage=1, max_damage=5)
    
    ability33 = Ability(name="AOE Heal",
                       description="AOE Heal Test. Used only by players.",
                       type=type4, mp_cost=5, is_myst_attack=False, is_heal=True, is_aoe=True, is_buff=False, min_damage=1, max_damage=5)

    Ability.objects.bulk_create([
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
    ])

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
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
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
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
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
        ability_3=ability3,
        ability_4=ability4,
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
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
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
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    GameUser.objects.bulk_create([
        gameuser1,
        gameuser2,
        gameuser3,
        gameuser4,
        gameuser5,
    ])

    # npcs + images
    npc1 = NPC(name="Narrator", image="logo.png")
    npc2 = NPC(name="Old Man", image="old-man.png")
    npc3 = NPC(name="Drunk Man 1", image="drunk-man-1.png")
    npc4 = NPC(name="Drunk Man 2", image="drunk-man-2.png")
    npc5 = NPC(name="Hilda", image="hilda.png")
    NPC.objects.bulk_create([
        npc1,
        npc2,
        npc3,
        npc4,
        npc5,
    ])

    # Enemies
    # TODO https://trello.com/c/0vbGueR2/204-chuck-create-enemy-images - Add enemy images
    # TODO https://trello.com/c/as5ukze5/203-create-enemy-abilities - Modify enemy abilities
    enemy1 = Enemy(
        name="Drunk Man 1",
        image="drunk-man-1.png",
        type=type1,
        start_hp=150,
        start_attack=50,
        start_defense=50,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy2 = Enemy(
        name="Drunk Man 2",
        image="drunk-man-2.png",
        type=type2,
        start_hp=150,
        start_attack=50,
        start_defense=50,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy3 = Enemy(
        name="Arachnid Sovereign",
        image="drunk-man-2.png",
        type=type4,
        start_hp=200,
        start_attack=60,
        start_defense=60,
        start_myst_attack=60,
        start_myst_defense=60,
        start_speed=60,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy4 = Enemy(
        name="Arachnid Minion",
        image="drunk-man-2.png",
        type=type4,
        start_hp=80,
        start_attack=40,
        start_defense=40,
        start_myst_attack=40,
        start_myst_defense=40,
        start_speed=75,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy5 = Enemy(
        name="Highland Revenant",
        image="drunk-man-2.png",
        type=type3,
        start_hp=200,
        start_attack=60,
        start_defense=60,
        start_myst_attack=60,
        start_myst_defense=60,
        start_speed=60,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy6 = Enemy(
        name="Highland Scion",
        image="drunk-man-2.png",
        type=type3,
        start_hp=80,
        start_attack=40,
        start_defense=40,
        start_myst_attack=40,
        start_myst_defense=40,
        start_speed=75,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy7 = Enemy(
        name="Primordial Anomaly",
        image="creature.png",
        type=type4,
        start_hp=300,
        start_attack=100,
        start_defense=100,
        start_myst_attack=100,
        start_myst_defense=100,
        start_speed=100,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy8 = Enemy(
        name="Luminar Sentinel",
        image="drunk-man-2.png",
        type=type1,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=50,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy9 = Enemy(
        name="Umbral Harbinger",
        image="drunk-man-2.png",
        type=type2,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=50,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy10 = Enemy(
        name="Granite Warden",
        image="drunk-man-2.png",
        type=type3,
        start_hp=100,
        start_attack=75,
        start_defense=75,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=50,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy11 = Enemy(
        name="Sylvan Enchanter",
        image="drunk-man-2.png",
        type=type4,
        start_hp=100,
        start_attack=75,
        start_defense=75,
        start_myst_attack=50,
        start_myst_defense=50,
        start_speed=75,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )
    enemy12 = Enemy(
        name="Galewing Shaman",
        image="drunk-man-2.png",
        type=type5,
        start_hp=100,
        start_attack=50,
        start_defense=50,
        start_myst_attack=75,
        start_myst_defense=75,
        start_speed=75,
        ability_1=ability1,
        ability_2=ability2,
        ability_3=ability3,
        ability_4=ability4,
    )

    Enemy.objects.bulk_create([
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
        enemy11,
        enemy12,
    ])

    # dialogue Act 1 Scene 1
    node1 = Dialogue(from_node_id=0, node_type="narration", speaker="Narrator", text="Your group finds themselves teleported to an abandoned alleyway in what looks like a quaint old village. The narrow passage is dimly lit, and the silence is broken by the distant sounds of chatter and laughter. Suddenly, two drunk men spot your group and stagger towards you, their eyes gleaming with mischief.", act=1, scene=1)
    node2 = Dialogue(from_node_id=1, node_type="talk", speaker="Drunk Man 1", text="Blimey, would ya look at this lot! Fancied themselves lost tourists, do they?", act=1, scene=1)
    node3 = Dialogue(from_node_id=2, node_type="talk", speaker="Drunk Man 2", text="Aven't seen faces like these 'round 'ere before!", act=1, scene=1)
    node4 = Dialogue(from_node_id=3, node_type="talk", speaker="Group Leader", text="We don't mean any harm. We're just passing through, gentlemen.", act=1, scene=1)
    node5 = Dialogue(from_node_id=4, node_type="talk", speaker="Drunk Man 1", text="Passin' through, eh? Not so fast! We don't get visitors often, so we might as well 'ave some fun with ya!", act=1, scene=1)
    node6 = Dialogue(from_node_id=5, node_type="talk", speaker="Group Leader", text="We don't want any trouble. We'll be on our way.", act=1, scene=1)
    node7 = Dialogue(from_node_id=6, node_type="talk", speaker="Drunk Man 2", text="Not so fast! You're stayin' put!", act=1, scene=1)
    node8 = Dialogue(from_node_id=7, node_type="talk", speaker="Old Man", text="Ey, what's all this ruckus?", act=1, scene=1)
    node9 = Dialogue(from_node_id=8, node_type="talk", speaker="Drunk Man 1", text="Stay out of this, old timer! These strangers are gonna get what's comin' to 'em!", act=1, scene=1)
    node10 = Dialogue(from_node_id=9, node_type="talk", speaker="Old Man", text="Now, now, lads. That's no way to treat our guests. Let 'em pass and be on their way.", act=1, scene=1)
    node11 = Dialogue(from_node_id=10, node_type="talk", speaker="Drunk Man 2", text="Fine, but they better not show their faces 'round here again!", act=1, scene=1)
    node12 = Dialogue(from_node_id=11, node_type="talk", speaker="Old Man", text="I apologize for their behavior. They can get a bit rowdy when they've 'ad a few too many. Please, come inside my tavern. You'll be safe there.", act=1, scene=1)
    node13 = Dialogue(from_node_id=12, node_type="talk", speaker="Group Leader", text="Thank you for your help. We'll gladly take shelter in your tavern.", act=1, scene=1)
    node14 = Dialogue(from_node_id=13, node_type="narration", speaker="Narrator", text="As your group hurries into the tavern, the old man closes the door behind you, shutting out the noise and tension from the alleyway.", act=1, scene=1)
    node15 = Dialogue(from_node_id=14, node_type="talk", speaker="Old Man", text="Sit, sit! Let me tell ya a tale of our plight. Evil creatures, they are. Taking control over our town, the last stronghold of good in our world. We need help, you see, from individuals not easily swayed by these beasts. And, it dawns on me, I believe you and your group might be the ones we've been waitin' for.", act=1, scene=1)
    node16 = Dialogue(from_node_id=15, node_type="talk", speaker="Group Leader", text="Us? Why us?", act=1, scene=1)
    node17 = Dialogue(from_node_id=16, node_type="talk", speaker="Old Man", text="Not entirely sure, my dear, but it seems fate has brought you here. We've been seekin' aid for a long time now, and you seem like a capable bunch. A band of mercenaries you ain't, but together, you make a good team.", act=1, scene=1)
    node18 = Dialogue(from_node_id=17, node_type="talk", speaker="Group Leader", text="How did we even end up in this village?", act=1, scene=1)
    node19 = Dialogue(from_node_id=18, node_type="talk", speaker="Old Man", text="Have another round, and I'll tell ya what I think. As for the 'how'... well, we're in a magical and mysterious place, ain't we? My guess is that you were brought here for a reason. The only way to defeat these creatures is with outside help, and you seem like the help we need.", act=1, scene=1)
    node20 = Dialogue(from_node_id=19, node_type="talk", speaker="Group Leader", text="Why now? Why did we end up here at this specific time?", act=1, scene=1)
    node21 = Dialogue(from_node_id=20, node_type="talk", speaker="Old Man", text="Time's runnin' out, I'm afraid. These creatures are changin', and it's not for the better. Other towns nearby have already felt their wrath. We're on the brink of losin' ourselves. You might just be our last hope.", act=1, scene=1)
    node22 = Dialogue(from_node_id=21, node_type="talk", speaker="Group Leader", text="But we're not warriors or fighters. We're {software developers}!", act=1, scene=1)
    node23 = Dialogue(from_node_id=22, node_type="talk", speaker="Old Man", text="Software developers, eh? I don't know much about that, but I believe you have somethin' within you. You'll find what you need to face this challenge. First things first, get a room upstairs in the tavern inn. In the morning, head to the general store and gather some equipment for your journey. You'll need it before you set off.", act=1, scene=1)
    
    # player decision
    node24 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Book a night at the inn and see what tomorrow brings", act=1, scene=1)
    node25 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Attempt to leave the tavern and try to get home", act=1, scene=1)
    node26 = Dialogue(from_node_id=23, node_type="player response", speaker="Group Leader", text="Continue to talk to the old man", act=1, scene=1)

    # node 24 Tree: Book a night at the inn and see what tomorrow brings
    node27 = Dialogue(from_node_id=24, node_type="talk", speaker="Group Leader", text="We've had quite a day. Maybe we should get some rest, see what tomorrow brings.", act=1, scene=1)
    node28 = Dialogue(from_node_id=27, node_type="talk", speaker="Group Member 1", text="It's been a lot to take in. A good night's rest might clear our heads.", act=1, scene=1)
    node29 = Dialogue(from_node_id=28, node_type="talk", speaker="Group Member 2", text="But what if we're really stuck here? We can't just wait around forever.", act=1, scene=1)
    node30 = Dialogue(from_node_id=29, node_type="talk", speaker="Group Leader", text="We'll keep our eyes and ears open. If there's a chance to find our way back, we'll take it. For now, let's book a night at the inn and regroup in the morning.", act=1, scene=1)
    node31 = Dialogue(from_node_id=30, node_type="narration", speaker="Narrator", text="As the group gets settled into their room above the tavern inn, they realize they have a window with a view into the very same alleyway they found themselves in earlier that evening.", act=1, scene=1)
    node32 = Dialogue(from_node_id=31, node_type="talk", speaker="Group Member 1", text="Hold on, everyone. Come take a look at this!", act=1, scene=1)
    node33 = Dialogue(from_node_id=32, node_type="talk", speaker="Group Member 2", text="What is it?", act=1, scene=1)
    node34 = Dialogue(from_node_id=33, node_type="talk", speaker="Group Member 1", text="It's the exact spot where we found ourselves transported! There's a weird glimmer in the air. I think we should investigate.", act=1, scene=1)
    node35 = Dialogue(from_node_id=34, node_type="talk", speaker="Group Leader", text="You're right. It's worth checking out. Let's head over there and see if we can find any clues.", act=1, scene=1)

    # node 25 Tree: Attempt to leave the tavern and try to get home
    node36 = Dialogue(from_node_id=25, node_type="talk", speaker="Group Member 1", text="We can't just sit around here hoping for answers. We need to go back to where we entered this place and look for clues. Maybe we'll find a way back home.", act=1, scene=1)
    node37 = Dialogue(from_node_id=36, node_type="talk", speaker="Group Member 2", text="I agree. It's worth a shot. We should at least try to retrace our steps.", act=1, scene=1)
    node38 = Dialogue(from_node_id=37, node_type="talk", speaker="Group Leader", text="Alright, it's settled then. Let's head back to the alley and see if we can find any clues.", act=1, scene=1)

    # node 26 Tree: Continue to talk to the old man
    node39 = Dialogue(from_node_id=26, node_type="narration", speaker="Narrator", text="The group debates their options, torn between waiting for answers and seeking a way back home. They turn back to the old man and he is passed out under the table.", act=1, scene=1)
    node40 = Dialogue(from_node_id=39, node_type="talk", speaker="Group Member 1", text="I think he's had a bit too much to drink. Maybe we should leave him be for now.", act=1, scene=1)
    node41 = Dialogue(from_node_id=40, node_type="talk", speaker="Group Leader", text="Agreed. Let's try to figure this out on our own for now.", act=1, scene=1)

    # 3 options lead to same choice
    node42 = Dialogue(from_node_id=35, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)
    node43 = Dialogue(from_node_id=38, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)
    node44 = Dialogue(from_node_id=41, node_type="narration", speaker="Narrator", text="They open the door to the tavern to leave and sense an unusual change in the air. Something inside them feels different—strength, confidence, or something else they can't quite grasp.", act=1, scene=1)

    # continuation of story from node 42
    node45 = Dialogue(from_node_id=42, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node46 = Dialogue(from_node_id=45, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node47 = Dialogue(from_node_id=46, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node48 = Dialogue(from_node_id=47, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node49 = Dialogue(from_node_id=48, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node50 = Dialogue(from_node_id=49, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    # continuation of story from node 43
    node51 = Dialogue(from_node_id=43, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node52 = Dialogue(from_node_id=51, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node53 = Dialogue(from_node_id=52, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node54 = Dialogue(from_node_id=53, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node55 = Dialogue(from_node_id=54, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node56 = Dialogue(from_node_id=55, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    # continuation of story from node 44
    node57 = Dialogue(from_node_id=44, node_type="talk", speaker="Group Leader", text="Do you guys feel that too? It's like there's something... different.", act=1, scene=1)
    node58 = Dialogue(from_node_id=57, node_type="talk", speaker="Group Member 1", text="Yeah, it's strange. I can't quite put my finger on it.", act=1, scene=1)
    node59 = Dialogue(from_node_id=58, node_type="talk", speaker="Group Member 2", text="Well, whatever it is, let's stay alert. We don't know what's out there.", act=1, scene=1)
    node60 = Dialogue(from_node_id=59, node_type="talk", speaker="Drunk Man 1", text="Look who's back for another beating!", act=1, scene=1)
    node61 = Dialogue(from_node_id=60, node_type="talk", speaker="Drunk Man 2", text="We warned ya to stay away!", act=1, scene=1)
    node62 = Dialogue(from_node_id=61, node_type="talk", speaker="Group Leader", text="We've had enough of this. Let's just take these guys out.", act=1, scene=1)

    Dialogue.objects.bulk_create([
        node1,
        node2,
        node3,
        node4,
        node5,
        node6,
        node7,
        node8,
        node9,
        node10,
        node11,
        node12,
        node13,
        node14,
        node15,
        node16,
        node17,
        node18,
        node19,
        node20,
        node21,
        node22,
        node23,
        node24,
        node25,
        node26,
        node27,
        node28,
        node29,
        node30,
        node31,
        node32,
        node33,
        node34,
        node35,
        node36,
        node37,
        node38,
        node39,
        node40,
        node41,
        node42,
        node43,
        node44,
        node45,
        node46,
        node47,
        node48,
        node49,
        node50,
        node51,
        node52,
        node53,
        node54,
        node55,
        node56,
        node57,
        node58,
        node59,
        node60,
        node61,
        node62,
    ])