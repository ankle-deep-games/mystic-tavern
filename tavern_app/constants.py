# Armor
ARCHMAGES_VESTMENTS = "Archmage's Vestments"
CLOTH_TUNIC = "Cloth Tunic"
ELVEN_WINDWRAP = "Elven Windwrap"
MAESTROS_TAILCOAT = "Maestro's Tailcoat"
RADIANT_VALOR_PLATE = "Radiant Valor Plate"
SORCERERS_ROBES = "Sorcerer's Robes"

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
ARCHER_ARMOR_1 = CLOTH_TUNIC
ARCHER_ARMOR_2 = ELVEN_WINDWRAP
ARCHER_ARMOR_3 = ELVEN_WINDWRAP
ARCHER_ABILITY_2 = SHATTER_SHOT
ARCHER_ABILITY_3 = SHADOW_VOLLEY

BARD_WEAPON_1 = WOOD_FLUTE
BARD_ARMOR_1 = CLOTH_TUNIC
BARD_ARMOR_2 = MAESTROS_TAILCOAT
BARD_ARMOR_3 = MAESTROS_TAILCOAT
BARD_ABILITY_2 = ANTHEM_OF_VALOR
BARD_ABILITY_3 = RESONANT_STONES

BLACKMAGE_WEAPON_1 = WOOD_STAFF
BLACKMAGE_ARMOR_1 = CLOTH_TUNIC
BLACKMAGE_ARMOR_2 = SORCERERS_ROBES
BLACKMAGE_ARMOR_3 = SORCERERS_ROBES
BLACKMAGE_ABILITY_2 = SHADOW_BLAST
BLACKMAGE_ABILITY_3 = ENCHANTED_GROVE

PALADIN_WEAPON_1 = WOOD_SWORD
PALADIN_ARMOR_1 = CLOTH_TUNIC
PALADIN_ARMOR_2 = RADIANT_VALOR_PLATE
PALADIN_ARMOR_3 = RADIANT_VALOR_PLATE
PALADIN_ABILITY_2 = SHIELD_BASH
PALADIN_ABILITY_3 = DIVINE_STRIKE

WHITEMAGE_WEAPON_1 = WOOD_STAFF
WHITEMAGE_ARMOR_1 = CLOTH_TUNIC
WHITEMAGE_ARMOR_2 = ARCHMAGES_VESTMENTS
WHITEMAGE_ARMOR_3 = ARCHMAGES_VESTMENTS
WHITEMAGE_ABILITY_2 = DIVINE_LIGHT
WHITEMAGE_ABILITY_3 = GALE_FURY

# TODO all keys and correct values https://trello.com/c/JRQnFXF9/292-finalize-all-regex-replace-values-once-dialogue-is-complete
ROLE_GAME_PROGRESSION_DICT = {
    "ARCHER": {
        "weapon1": ARCHER_WEAPON_1,
        "armor1": ARCHER_ARMOR_1,
        "armor2": ARCHER_ARMOR_2,
        "armor3": ARCHER_ARMOR_3,
        "short_role_summary": "dope shooter",
        "ability2": ARCHER_ABILITY_2,
        "ability3": ARCHER_ABILITY_3,
    },
    "BARD": {
        "weapon1": BARD_WEAPON_1,
        "armor1": BARD_ARMOR_1,
        "armor2": BARD_ARMOR_2,
        "armor3": BARD_ARMOR_3,
        "short_role_summary": "dope musician",
        "ability2": BARD_ABILITY_2,
        "ability3": BARD_ABILITY_3,
    },
    "BLACKMAGE": {
        "weapon1": BLACKMAGE_WEAPON_1,
        "armor1": BLACKMAGE_ARMOR_1,
        "armor2": BLACKMAGE_ARMOR_2,
        "armor3": BLACKMAGE_ARMOR_3,
        "short_role_summary": "dope mage",
        "ability2": BLACKMAGE_ABILITY_2,
        "ability3": BLACKMAGE_ABILITY_3,
    },
    "PALADIN": {
        "weapon1": PALADIN_WEAPON_1,
        "armor1": PALADIN_ARMOR_1,
        "armor2": PALADIN_ARMOR_2,
        "armor3": PALADIN_ARMOR_3,
        "short_role_summary": "dope fighter",
        "ability2": PALADIN_ABILITY_2,
        "ability3": PALADIN_ABILITY_3,
    },
    "WHITEMAGE": {
        "weapon1": WHITEMAGE_WEAPON_1,
        "armor1": WHITEMAGE_ARMOR_1,
        "armor2": WHITEMAGE_ARMOR_2,
        "armor3": WHITEMAGE_ARMOR_3,
        "short_role_summary": "dope healer",
        "ability2": WHITEMAGE_ABILITY_2,
        "ability3": WHITEMAGE_ABILITY_3,
    },
}

# TODO real quest nodes https://trello.com/c/7ohf05pK/250-finalize-weapon-armor-ability-assignments-for-each-role-and-assign-them-in-the-code-as-game-progresses
# Dialogue pk/ids of important nodes used for game flow in views.scene
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
