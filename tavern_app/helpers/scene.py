import re

from ..models import Game, GameUser, NPC, GameDialogue, Dialogue


def get_character_list(game: Game) -> list:
    """combines players and npcs into a single list that can later be used to add names and images to dialogues"""
    character_list = []
    game_users = GameUser.objects.filter(game=game)

    # in dialogue we save speakers as player1 - player4
    # at run time compare those against players in the game, so we can display the player username
    for idx, game_user in enumerate(game_users):
        speaker = ""
        if idx == 0:
            speaker = "player1"
        elif idx == 1:
            speaker = "player2"
        elif idx == 2:
            speaker = "player3"
        elif idx == 3:
            speaker = "player4"
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
        game: Game, game_dialogue_progress_list: list, character_list: list, act: int, scene_num: int
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

            # TODO here to show it next
            replaced_text = check_and_regex_replace_dialogue(game, dialogue)

            next_dialogue_list.append(
                {
                    "id": dialogue.pk,
                    "from_node_id": dialogue.from_node_id,
                    "node_type": dialogue.node_type,
                    "name": name,
                    "text": replaced_text,
                    "image": image,
                }
            )

    return next_dialogue_list


def check_and_regex_replace_dialogue(game, dialogue):
    d_id = dialogue.pk

    if d_id == 2:
        player_num_to_regex = '1'

    # empty list to store dict for each gu
    gu_list = []
    player_num = 1  # Initialize a counter for player numbers

    gameusers_queryset = GameUser.objects.filter(game=game)

    for index, gu in enumerate(gameusers_queryset, start=1):
        weapon1 = "Default Weapon"
        armor1 = "Default Armor"
        short_description = "Default Description"

        if gu.role.name == 'WHITEMAGE':
            weapon1 = 'Wood Staff'
            armor1 = "Cloth Tunic"
            short_description = "dope healer"  # TODO
        elif gu.role.name == 'BLACKMAGE':
            weapon1 = 'Wood Staff'
            armor1 = "Cloth Tunic"
            short_description = "dope mage"
        elif gu.role.name == 'BARD':
            weapon1 = 'Wood Flute'
            armor1 = "Cloth Tunic"
            short_description = "dope musician"  # TODO
        elif gu.role.name == 'PALADIN':
            weapon1 = 'Wood Sword'
            armor1 = "Cloth Tunic"
            short_description = "dope fighter"  # TODO
        elif gu.role.name == 'ARCHER':
            weapon1 = 'Wood Bow'
            armor1 = "Cloth Tunic"
            short_description = "dope shooter"  # TODO

        gu_dict = {
            f'player{player_num}': gu.user.username,
            'role': gu.role.display_name,
            'weapon1': weapon1,
            'armor1': armor1,
            'short_role_summary': short_description,
            'player_num_name': f'player{player_num}',
        }
        gu_list.append(gu_dict)

        player_num += 1  # Increment the player number for the next iteration

    # The text template
    text_template = dialogue.text

    # Find the dictionary with 'player_num_name' = 'player1'
    current_player = next((player for player in gu_list if player['player_num_name'] == f'player{player_num_to_regex}'), None)

    # Regex pattern to match text within curly braces {}
    pattern = r"{([^{}]*)}"

    # Find all matches within the text template
    matches = re.findall(pattern, text_template)

    # Replace placeholders in the text_template with values from current_player
    replaced_text = text_template
    if current_player:
        for match in matches:
            if match in current_player:
                replaced_text = replaced_text.replace("{" + match + "}", str(current_player[match]))

    return replaced_text
