from ..models import GameUser, Ability


def gameuser_grant_ability(gameuser: GameUser, ability: Ability, slot: int) -> None:
    gameuser = GameUser.objects.get(pk=gameuser.pk)
    if slot == 1:
        gameuser.ability_1 = ability
    elif slot == 2:
        gameuser.ability_2 = ability
    elif slot == 3:
        gameuser.ability_3 = ability
    elif slot == 4:
        gameuser.ability_4 = ability

    gameuser.save()
