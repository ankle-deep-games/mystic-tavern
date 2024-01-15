# Armor
CLOTH_TUNIC = 'Cloth Tunic'

# Weapon
WOOD_STAFF = 'Wood Staff'

# Abilities
DIVINE_LIGHT = 'Divine Light'
GALE_FURY = 'Gale Fury'
SHADOW_BLAST = 'Shadow Blast'

# Role Armor / Weapons
WHITEMAGE_WEAPON_1 = WOOD_STAFF
WHITEMAGE_ARMOR_1 = CLOTH_TUNIC
WHITEMAGE_ABILITY_2 = DIVINE_LIGHT
WHITEMAGE_ABILITY_3 = GALE_FURY

BLACKMAGE_WEAPON_1 = WOOD_STAFF
BLACKMAGE_ARMOR_1 = CLOTH_TUNIC
BLACKMAGE_ABILITY_2 = DIVINE_LIGHT
BLACKMAGE_ABILITY_3 = GALE_FURY

# TODO all keys and correct values https://trello.com/c/JRQnFXF9/292-finalize-all-regex-replace-values-once-dialogue-is-complete
ROLE_GAME_PROGRESSION_DICT = {
    'WHITEMAGE': {
        'weapon1': WHITEMAGE_WEAPON_1,
        'armor1': WHITEMAGE_ARMOR_1,
        'short_role_summary': 'dope healer',
        'ability2': WHITEMAGE_ABILITY_2,
        'ability3': GALE_FURY,
    },
    'BLACKMAGE': {
        'weapon1': 'Wood Staff',
        'armor1': CLOTH_TUNIC,
        'short_role_summary': 'dope mage',
        'ability2': SHADOW_BLAST,
    },
    'BARD': {
        'weapon1': 'Wood Flute',
        'armor1': CLOTH_TUNIC,
        'short_role_summary': 'dope musician',
        'ability2': 'Anthem of Valor',
    },
    'PALADIN': {
        'weapon1': 'Wood Sword',
        'armor1': CLOTH_TUNIC,
        'short_role_summary': 'dope fighter',
        'ability2': 'Shield Bash',
    },
    'ARCHER': {
        'weapon1': 'Wood Bow',
        'armor1': CLOTH_TUNIC,
        'short_role_summary': 'dope shooter',
        'ability2': 'Shatter Shot',
    },
}

# Dialogue pk
QUEST_1_NODE = 3
QUEST_2_NODE = 4
QUEST_3_NODE = 5
