from ..models import Game, GameUser, NPC, GameDialogue, Dialogue


def get_character_list(game: Game) -> list:
    """combines players and npcs into a single list that can later be used to add names and images to dialogues"""
    character_list = []
    game_users = GameUser.objects.filter(game=game)

    # in dialogue we save speakers as "Group Leader" or "Group Member 1"
    # at run time compare those against players in the game, so we can display the player username
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
        character_list.append(
            {"name": game_user.name(), "image": game_user.image(), "speaker": speaker}
        )

    npcs = NPC.objects.all()
    for npc in npcs:
        character_list.append(
            {"name": npc.name, "image": npc.image, "speaker": npc.name}
        )

    return character_list


def get_game_dialogue_progress_list(
        character_list: list, game_id: int, act: int, scene_num: int
) -> list:
    """current game/act/scene dialogue + names and images LAST 2 NODES"""
    game_dialogue_progress_list = []
    game_dialogue_progress = GameDialogue.objects.filter(game=game_id)
    for game_dialogue in game_dialogue_progress:
        # only build the list for the current act and scene
        if (
                game_dialogue.dialogue.act == act
                and game_dialogue.dialogue.scene == scene_num
        ):
            name = ""
            image = ""
            for char in character_list:
                if char["speaker"] == game_dialogue.dialogue.speaker:
                    name = char["name"]
                    image = char["image"]

            game_dialogue_progress_list.append(
                {
                    "id": game_dialogue.dialogue.pk,
                    "node_type": game_dialogue.dialogue.node_type,
                    "name": name,
                    "text": game_dialogue.dialogue.text,
                    "image": image,
                }
            )

    return game_dialogue_progress_list[-2:]


def get_next_dialogue_list(
        game_dialogue_progress_list: list, character_list: list, act: int, scene_num: int
) -> list:
    """queries the game dialogue progress for the next single dialogue or multiple player dialogue choices"""
    next_dialogue_list = []
    # make sure this act/scene has at least 1 node to prevent errors. filter by act and scene.
    if len(game_dialogue_progress_list) > 0:
        next_dialogue = Dialogue.objects.filter(
            from_node_id=game_dialogue_progress_list[-1]["id"], act=act, scene=scene_num
        )
        for dialogue in next_dialogue:
            name = ""
            image = ""
            for char in character_list:
                if char["speaker"] == dialogue.speaker:
                    name = char["name"]
                    image = char["image"]

            next_dialogue_list.append(
                {
                    "id": dialogue.pk,
                    "from_node_id": dialogue.from_node_id,
                    "node_type": dialogue.node_type,
                    "name": name,
                    "text": dialogue.text,
                    "image": image,
                }
            )

    return next_dialogue_list


def plant_seed_decision():
    print("PLANTING THE SEED PLACEHOLDER")
    # This will do something like: somehow we keep track of which gem was planted.
    # randomly assign the 4 players one of the gems and give them the corresponding ability
    # we don't want to assign someone the TYPE of gem that their role is
