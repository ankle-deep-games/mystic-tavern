from ..models import Game, GameUser, NPC, GameDialogue, Dialogue
import random

def get_character_list(game: Game) -> list:
    """combines players and npcs into a single list that can later be used to add names and images to dialogues"""
    character_list = []
    game_users = GameUser.objects.filter(game=game)
    
    # in dialogue we save speakers as "Group Leader" or "Group Member 1"
    # at run time compare those against players in the game so we can display the player username
    for idx, game_user in enumerate(game_users):
        speaker = ""
        if idx == 0:
            speaker = "Group Leader"
        elif idx == 1:
            speaker = "Group Member 1"
        elif idx == 2:
            speaker = "Group Member 2"
        elif idx == 3:
            speaker = "Group Member 3"
        character_list.append({'name': game_user.name(), 'image': game_user.image(), 'speaker': speaker})

    npcs = NPC.objects.all()
    for npc in npcs:
        character_list.append({'name': npc.name, 'image': npc.image, 'speaker': npc.name})

    return character_list

def get_game_dialogue_progress_list(character_list: list, game_id: int, act: int, scene_num: int) -> list:
    """current game/act/scene dialogue + names and images"""
    game_dialogue_progress_list = []
    game_dialogue_progress = GameDialogue.objects.filter(game=game_id)
    for game_dialogue in game_dialogue_progress:
        # only build the list for the current act and scene
        if game_dialogue.dialogue.act == act and game_dialogue.dialogue.scene == scene_num:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == game_dialogue.dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            game_dialogue_progress_list.append({
                'id': game_dialogue.dialogue.pk,
                'node_type': game_dialogue.dialogue.node_type,
                'name': name,
                'text': game_dialogue.dialogue.text,
                'image': image,
                })
            
    return game_dialogue_progress_list

def get_next_dialogue_list(game_dialogue_progress_list: list, character_list: list, act: int, scene_num: int) -> list:
    """queries the game dialogue progress for the next single dialogue or multiple player dialogue choices"""
    next_dialogue_list = []
    # make sure this act/scene has at least 1 node to prevent errors. filter by act and scene.
    if len(game_dialogue_progress_list) > 0:
        next_dialogue = Dialogue.objects.filter(from_node_id=game_dialogue_progress_list[-1]['id'], act=act, scene=scene_num)
        for dialogue in next_dialogue:
            name = ""
            image = ""
            for char in character_list:
                if char['speaker'] == dialogue.speaker:
                    name = char['name']
                    image = char['image']
            
            next_dialogue_list.append({
                'id': dialogue.pk,
                'from_node_id': dialogue.from_node_id,
                'node_type': dialogue.node_type,
                'name': name,
                'text': dialogue.text,
                'image': image,
                })
    
    return next_dialogue_list

def plant_seed_decision(gameuser_dict, crystal_choice):
    """
    :param gameuser_dict: A dictionary of gameusers and their associated role_id's in this format: {"player_1": 1}
    :param crystal_choice: A string variable with these enumerations: White, Black, Grey, Green, Light Blue

    This function will take in a gameuser_dict that is expected to have gameuser_id and role.type_id, and it will also
    take in the crystal_choice of the group. It will randomly assign the crystals (and corresponding abilities) to the
    gameusers until verification that the crystal does not match the role type of the user.

    return: player_abilities_dict in this format: {"player_1": {'role_id': 1, 'crystal': 'Black', 'ability': 'Dark Embrace'}
    """
    # Hardcoding crystal options for MVP
    crystal_options_dict = {'White': 1, 'Black': 2, 'Grey': 3, 'Green': 4, 'Light Blue': 5}

    # Delete the group's crystal choice for crystal and ability assignment purposes
    del crystal_options_dict[crystal_choice]

    # Make a list of crystal strings from the dict
    crystal_options_list = list(crystal_options_dict.keys())

    gameuser_crystal_dict = {}

    # For each item in the dict, get a random crystal and assign to player once verifying that it doesn't match the
    # players role type
    for player, role_id in gameuser_dict.items():
        crystal = random.choice(crystal_options_list)

        while crystal_options_dict[crystal] == role_id:
            crystal = random.choice(crystal_options_list)

        crystal_options_list.remove(crystal)

        gameuser_crystal_dict[player] = {"role_id": role_id, "crystal": crystal}

    # Role ID + Crystal ability assignments
    abilities_dict = {
        1: {
            'Black': 'Dark Embrace',
            'Grey': 'Stoneguard',
            'Green': 'Thorned Grasp',
            'Light Blue': 'Gale Fury'
        },
        2: {
            'White': 'Radiant Surge',
            'Grey': 'Petrifying Blast',
            'Green': 'Sylvan Whispers',
            'Light Blue': 'Tempest Nova'
        },
        3: {
            'White': 'Divine Strike',
            'Black': 'Shadow Strike',
            'Green': 'Timber Slam',
            'Light Blue': 'Cyclone Slash'
        },
        4: {
            'White': 'Natures Embrace',
            'Black': 'Shadow Volley',
            'Grey': 'Piercing Arrow',
            'Light Blue': 'Storm of Arrows'
        },
        5: {
            'White': 'Luminous Sonata',
            'Black': 'Ebon Serenade',
            'Grey': 'Resonant Stones',
            'Green': 'Enchanted Grove'
        }
    }

    player_abilities_dict = {}

    for player, data in gameuser_crystal_dict.items():
        role_id = data['role_id']
        crystal = data['crystal']

        ability = abilities_dict[role_id][crystal]

        player_abilities_dict[player] = {
            'role_id': role_id,
            'crystal': crystal,
            'ability': ability
        }

    return player_abilities_dict
