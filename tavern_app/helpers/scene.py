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
                    "text": game_dialogue.get_display_text(),
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


def get_default_role_attributes(role_name: str) -> dict:
    """Returns default attributes based on the role name."""
    # TODO all keys and correct values https://trello.com/c/JRQnFXF9/292-finalize-all-regex-replace-values-once-dialogue-is-complete
    default_attributes = {
        'WHITEMAGE': {'weapon1': 'Wood Staff', 'armor1': 'Cloth Tunic', 'short_role_summary': 'dope healer',
                      'ability2': 'Divine Light'},
        'BLACKMAGE': {'weapon1': 'Wood Staff', 'armor1': 'Cloth Tunic', 'short_role_summary': 'dope mage',
                      'ability2': 'Arcane Blast'},
        'BARD': {'weapon1': 'Wood Flute', 'armor1': 'Cloth Tunic', 'short_role_summary': 'dope musician',
                 'ability2': 'Anthem of Valor'},
        'PALADIN': {'weapon1': 'Wood Sword', 'armor1': 'Cloth Tunic', 'short_role_summary': 'dope fighter',
                    'ability2': 'Shield Bash'},
        'ARCHER': {'weapon1': 'Wood Bow', 'armor1': 'Cloth Tunic', 'short_role_summary': 'dope shooter',
                   'ability2': 'Shatter Shot'},
    }
    return default_attributes.get(role_name, {'weapon1': 'Default Weapon', 'armor1': 'Default Armor',
                                              'short_role_summary': 'Default Description',
                                              'ability2': 'Default Ability 2'})


def build_game_user_dict(gameuser: GameUser, player_num: int) -> dict:
    """Constructs a dictionary of GameUser attributes."""
    role_attributes = get_default_role_attributes(gameuser.role.name)
    return {
        f'player{player_num}': gameuser.user.username,
        'role': gameuser.role.display_name,
        'weapon1': role_attributes['weapon1'],
        'armor1': role_attributes['armor1'],
        'short_role_summary': role_attributes['short_role_summary'],
        'ability2': role_attributes['ability2'],
    }


def replace_dialogue_placeholders(dialogue_text: str, placeholders: dict) -> str:
    """Replaces placeholders in the dialogue text with actual values."""
    pattern = r"{([^{}]*)}"
    matches = re.findall(pattern, dialogue_text)
    replaced_text = dialogue_text

    for match in matches:
        if match in placeholders:
            replaced_text = replaced_text.replace("{" + match + "}", str(placeholders[match]))

    return replaced_text


def check_and_regex_replace_dialogue(game: Game, dialogue: Dialogue) -> str:
    """Processes and replaces placeholders in dialogue data."""
    # TODO assign correct nodes https://trello.com/c/GqoKIApr/293-assign-regex-replace-on-final-nodes
    # if dialogue.pk in [2, 3]:
    #     current_player_key = 'player1'
    # elif dialogue.pk in [4, 5]:
    #     current_player_key = 'player2'
    # elif dialogue.pk in [6, 7]:
    #     current_player_key = 'player3'
    # elif dialogue.pk in [8, 9]:
    #     current_player_key = 'player4'
    # elif dialogue.pk == 10:
    #     # Handle specific case for dialogue.pk == 10, like the night decision
    #     return dialogue.text
    # else:
    #     # Return dialogue.text for any other case not explicitly handled above
    #     return dialogue.text
    return dialogue.text # remove line after TODO

    gameusers = GameUser.objects.filter(game=game)
    gameuser_dicts = [build_game_user_dict(gu, index) for index, gu in enumerate(gameusers, start=1)]

    # Find the dictionary for the current player using the player number
    current_player = next(player for player in gameuser_dicts if current_player_key in player)

    return replace_dialogue_placeholders(dialogue.text, current_player)
