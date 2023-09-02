from django.contrib import admin
from .models import Game, GameUser, Role, Gender, Weapon, Armor, Ability, Dialogue, GameDialogue, NPC, Type, Enemy, GameEnemy, CombatLog, GameScene, GameTurnOrder

admin.site.register(Game)
admin.site.register(GameUser)
admin.site.register(Role)
admin.site.register(Gender)
admin.site.register(Weapon)
admin.site.register(Armor)
admin.site.register(Ability)
admin.site.register(Dialogue)
admin.site.register(GameDialogue)
admin.site.register(NPC)
admin.site.register(Type)
admin.site.register(Enemy)
admin.site.register(GameEnemy)
admin.site.register(CombatLog)
admin.site.register(GameScene)
admin.site.register(GameTurnOrder)
