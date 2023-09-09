from ..models import Game, GameUser, NPC

def get_character_list(game: Game):
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