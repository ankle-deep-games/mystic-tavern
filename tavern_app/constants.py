# Armor
ARCHMAGES_VESTMENTS = "Archmage's Vestments"
CELESTIAL_CIRCLET = "Celestial Circlet"
CLOTH_TUNIC = "Cloth Tunic"
ELVEN_WINDWRAP = "Elven Windwrap"
FALCONERS_BRACERS = "Falconer's Bracers"
HARMONISTS_CUMMERBUND = "Harmonist's Cummerbund"
MAESTROS_TAILCOAT = "Maestro's Tailcoat"
RADIANT_CUIRASS = "Radiant Cuirass"
SHADOWWEAVE_CAPE = "Shadowweave Cape"
SORCERERS_ROBES = "Sorcerer's Robes"
VALOR_SHIELD = "Valor Shield"

# Weapon
IVORY_ROD = "Ivory Rod"
LONGBOW = "Longbow"
LONGSWORD = "Longsword"
MELODIOUS_LUTE = "Melodious Lute"
OBSIDIAN_WAND = "Obsidian Wand"
WOOD_BOW = "Wood Bow"
WOOD_FLUTE = "Wood Flute"
WOOD_STAFF = "Wood Staff"
WOOD_SWORD = "Wood Sword"

# Abilities
ANTHEM_OF_VALOR = "Anthem of Valor"
ARCANE_DARKNESS = "Arcane Darkness"
ATTACK = "Attack"
DIVINE_LIGHT = "Divine Light"
DIVINE_STRIKE = "Divine Strike"
ENCHANTED_GROVE = "Enchanted Grove"
ETHEREAL_CRESCENDO = "Ethereal Crescendo"
GALE_FURY = "Gale Fury"
GROVES_VENGEANCE = "Grove's Vengeance"
HOLY_WRATH = "Holy Wrath"
RESONANT_STONES = "Resonant Stones"
SANCTUARY = "Sanctuary"
SHADOW_BLAST = "Shadow Blast"
SHADOW_VOLLEY = "Shadow Volley"
SHATTER_SHOT = "Shatter Shot"
SHIELD_BASH = "Shield Bash"

# Role Armor / Weapons
# TODO assign correct values https://trello.com/c/7ohf05pK/250-finalize-weapon-armor-ability-assignments-for-each-role-and-assign-them-in-the-code-as-game-progresses
ARCHER_WEAPON_1 = WOOD_BOW
ARCHER_WEAPON_2 = LONGBOW
ARCHER_ARMOR_1 = CLOTH_TUNIC
ARCHER_ARMOR_2 = ELVEN_WINDWRAP
ARCHER_ARMOR_3 = FALCONERS_BRACERS
ARCHER_ABILITY_2 = SHATTER_SHOT
ARCHER_ABILITY_3 = SHADOW_VOLLEY
ARCHER_ABILITY_4 = GROVES_VENGEANCE

BARD_WEAPON_1 = WOOD_FLUTE
BARD_WEAPON_2 = MELODIOUS_LUTE
BARD_ARMOR_1 = CLOTH_TUNIC
BARD_ARMOR_2 = MAESTROS_TAILCOAT
BARD_ARMOR_3 = HARMONISTS_CUMMERBUND
BARD_ABILITY_2 = ANTHEM_OF_VALOR
BARD_ABILITY_3 = RESONANT_STONES
BARD_ABILITY_4 = ETHEREAL_CRESCENDO

BLACKMAGE_WEAPON_1 = WOOD_STAFF
BLACKMAGE_WEAPON_2 = OBSIDIAN_WAND
BLACKMAGE_ARMOR_1 = CLOTH_TUNIC
BLACKMAGE_ARMOR_2 = SORCERERS_ROBES
BLACKMAGE_ARMOR_3 = SHADOWWEAVE_CAPE
BLACKMAGE_ABILITY_2 = SHADOW_BLAST
BLACKMAGE_ABILITY_3 = ENCHANTED_GROVE
BLACKMAGE_ABILITY_4 = ARCANE_DARKNESS

PALADIN_WEAPON_1 = WOOD_SWORD
PALADIN_WEAPON_2 = LONGSWORD
PALADIN_ARMOR_1 = CLOTH_TUNIC
PALADIN_ARMOR_2 = RADIANT_CUIRASS
PALADIN_ARMOR_3 = VALOR_SHIELD
PALADIN_ABILITY_2 = SHIELD_BASH
PALADIN_ABILITY_3 = DIVINE_STRIKE
PALADIN_ABILITY_4 = HOLY_WRATH

WHITEMAGE_WEAPON_1 = WOOD_STAFF
WHITEMAGE_WEAPON_2 = IVORY_ROD
WHITEMAGE_ARMOR_1 = CLOTH_TUNIC
WHITEMAGE_ARMOR_2 = ARCHMAGES_VESTMENTS
WHITEMAGE_ARMOR_3 = CELESTIAL_CIRCLET
WHITEMAGE_ABILITY_2 = DIVINE_LIGHT
WHITEMAGE_ABILITY_3 = GALE_FURY
WHITEMAGE_ABILITY_4 = SANCTUARY

# TODO all keys and correct values https://trello.com/c/JRQnFXF9/292-finalize-all-regex-replace-values-once-dialogue-is-complete
ROLE_GAME_PROGRESSION_DICT = {
    "ARCHER": {
        "weapon1": ARCHER_WEAPON_1,
        "weapon2": ARCHER_WEAPON_2,
        "armor1": ARCHER_ARMOR_1,
        "armor2": ARCHER_ARMOR_2,
        "armor3": ARCHER_ARMOR_3,
        "short_role_summary": "The Archer, a sharpshooter with a mighty bow, knocks ‘em dead from a distance, givin’ a "
                              "hand to their mates in bloody fights with eagle eyes and quick feet.",
        "ability2": ARCHER_ABILITY_2,
        "ability3": ARCHER_ABILITY_3,
        "ability4": ARCHER_ABILITY_4,
    },
    "BARD": {
        "weapon1": BARD_WEAPON_1,
        "weapon2": BARD_WEAPON_2,
        "armor1": BARD_ARMOR_1,
        "armor2": BARD_ARMOR_2,
        "armor3": BARD_ARMOR_3,
        "short_role_summary": "The Bard, a charming and handy helper, plays music and tells stories. They cheer up "
                              "their mates with happy tunes and thrilling tales, makin’ them brave and strong. "
                              "Bards are good at changin’ the fight and helpin’ out, keepin’ their team keen and "
                              "prepared for any trouble ahead.",
        "ability2": BARD_ABILITY_2,
        "ability3": BARD_ABILITY_3,
        "ability4": BARD_ABILITY_4,
    },
    "BLACKMAGE": {
        "weapon1": BLACKMAGE_WEAPON_1,
        "weapon2": BLACKMAGE_WEAPON_2,
        "armor1": BLACKMAGE_ARMOR_1,
        "armor2": BLACKMAGE_ARMOR_2,
        "armor3": BLACKMAGE_ARMOR_3,
        "short_role_summary": "The Black Mage, a master of magic, holds a staff buzzin’ with dark power, blastin’ "
                              "enemies from far away with wicked spells. Black Mages cast complex curses, summonin’ "
                              "nasty things and twistin’ the laws of nature to destroy their enemies from afar.",
        "ability2": BLACKMAGE_ABILITY_2,
        "ability3": BLACKMAGE_ABILITY_3,
        "ability4": BLACKMAGE_ABILITY_4,
    },
    "PALADIN": {
        "weapon1": PALADIN_WEAPON_1,
        "weapon2": PALADIN_WEAPON_2,
        "armor1": PALADIN_ARMOR_1,
        "armor2": PALADIN_ARMOR_2,
        "armor3": PALADIN_ARMOR_3,
        "short_role_summary": "The Paladin, a brave and strong fighter, wears thick armor and brandishes a gleaming "
                              "sword and shield. They’re good at bashin’ enemies up close, crushin’ them with mighty "
                              "blows. Paladins are famous for their grit, protectin’ their friends from danger and "
                              "just straight out stormin’ the evil bastards!",
        "ability2": PALADIN_ABILITY_2,
        "ability3": PALADIN_ABILITY_3,
        "ability4": PALADIN_ABILITY_4,
    },
    "WHITEMAGE": {
        "weapon1": WHITEMAGE_WEAPON_1,
        "weapon2": WHITEMAGE_WEAPON_2,
        "armor1": WHITEMAGE_ARMOR_1,
        "armor2": WHITEMAGE_ARMOR_2,
        "armor3": WHITEMAGE_ARMOR_3,
        "short_role_summary": "The White Mage, a healer and restorer, carries a staff and is versed in ancient magic. "
                              "They’re experts at fixin’ injuries and boostin’ their friends. White Mages use the "
                              "power of light, healin’ hurt bodies and fillin’ up energy, makin’ sure their team "
                              "stays tough and ready on their dangerous adventure.",
        "ability2": WHITEMAGE_ABILITY_2,
        "ability3": WHITEMAGE_ABILITY_3,
        "ability4": WHITEMAGE_ABILITY_4,
    },
}

# Scene starting and ending nodes
ACT_1_SCENE_1_ENDING_NODE = 13

ACT_1_SCENE_2_STARTING_NODE = 14

# TODO real quest nodes https://trello.com/c/7ohf05pK/250-finalize-weapon-armor-ability-assignments-for-each-role-and-assign-them-in-the-code-as-game-progresses
# Dialogue pk/ids of important nodes used for game flow in views.scene
PLAYER_1_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE = 202
PLAYER_1_RESULT_WEAPON1_ARMOR1_ABILITY2_NODE = 202
PLAYER_2_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE = 204
PLAYER_2_RESULT_WEAPON1_ARMOR1_ABILITY2_NODE = 205
PLAYER_3_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE = 206
PLAYER_3_RESULT_WEAPON1_ARMOR1_ABILITY2_NODE = 207
PLAYER_4_GRANT_WEAPON1_ARMOR1_ABILITY2_NODE = 208
PLAYER_4_RESULT_WEAPON1_ARMOR1_ABILITY2_NODE = 209

PLAYER_1_WEAPON_UPGRADE_NODE = 303
PLAYER_2_WEAPON_UPGRADE_NODE = 304
PLAYER_3_WEAPON_UPGRADE_NODE = 305
PLAYER_4_WEAPON_UPGRADE_NODE = 306

END_OF_SCENE_1_NODES = [58, 65, 72]

QUEST_1_NODE = 101
QUEST_2_NODE = 102
QUEST_3_NODE = 103

NIGHT_DECISION_ALL_REST_NODE = 104
NIGHT_DECISION_ROTATE_REST_NODE = 105
NIGHT_DECISION_PLAYER_1_WATCH_NODE = 106
NIGHT_DECISION_PLAYER_2_WATCH_NODE = 107
NIGHT_DECISION_PLAYER_3_WATCH_NODE = 108
NIGHT_DECISION_PLAYER_4_WATCH_NODE = 109
