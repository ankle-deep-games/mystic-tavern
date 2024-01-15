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
ARCHER_WEAPON_1 = WOOD_BOW
ARCHER_ARMOR_1 = CLOTH_TUNIC
ARCHER_ABILITY_2 = SHATTER_SHOT
ARCHER_ABILITY_3 = SHADOW_VOLLEY

BARD_WEAPON_1 = WOOD_FLUTE
BARD_ARMOR_1 = CLOTH_TUNIC
BARD_ABILITY_2 = ANTHEM_OF_VALOR
BARD_ABILITY_3 = RESONANT_STONES

BLACKMAGE_WEAPON_1 = WOOD_STAFF
BLACKMAGE_ARMOR_1 = CLOTH_TUNIC
BLACKMAGE_ABILITY_2 = SHADOW_BLAST
BLACKMAGE_ABILITY_3 = ENCHANTED_GROVE

PALADIN_WEAPON_1 = WOOD_SWORD
PALADIN_ARMOR_1 = CLOTH_TUNIC
PALADIN_ABILITY_2 = SHIELD_BASH
PALADIN_ABILITY_3 = DIVINE_STRIKE

WHITEMAGE_WEAPON_1 = WOOD_STAFF
WHITEMAGE_ARMOR_1 = CLOTH_TUNIC
WHITEMAGE_ABILITY_2 = DIVINE_LIGHT
WHITEMAGE_ABILITY_3 = GALE_FURY

# TODO all keys and correct values
# https://trello.com/c/JRQnFXF9/292-finalize-all-regex-replace-values-once-dialogue-is-complete
ROLE_GAME_PROGRESSION_DICT = {
    "ARCHER": {
        "weapon1": ARCHER_WEAPON_1,
        "armor1": ARCHER_ARMOR_1,
        "short_role_summary": "dope shooter",
        "ability2": ARCHER_ABILITY_2,
        "ability3": ARCHER_ABILITY_3,
    },
    "BARD": {
        "weapon1": BARD_WEAPON_1,
        "armor1": BARD_ARMOR_1,
        "short_role_summary": "dope musician",
        "ability2": BARD_ABILITY_2,
        "ability3": BARD_ABILITY_3,
    },
    "BLACKMAGE": {
        "weapon1": BLACKMAGE_WEAPON_1,
        "armor1": BLACKMAGE_ARMOR_1,
        "short_role_summary": "dope mage",
        "ability2": BLACKMAGE_ABILITY_2,
        "ability3": BLACKMAGE_ABILITY_3,
    },
    "PALADIN": {
        "weapon1": PALADIN_WEAPON_1,
        "armor1": PALADIN_ARMOR_1,
        "short_role_summary": "dope fighter",
        "ability2": PALADIN_ABILITY_2,
        "ability3": PALADIN_ABILITY_3,
    },
    "WHITEMAGE": {
        "weapon1": WHITEMAGE_WEAPON_1,
        "armor1": WHITEMAGE_ARMOR_1,
        "short_role_summary": "dope healer",
        "ability2": WHITEMAGE_ABILITY_2,
        "ability3": WHITEMAGE_ABILITY_3,
    },
}

# Dialogue pk
QUEST_1_NODE = 3
QUEST_2_NODE = 4
QUEST_3_NODE = 5
