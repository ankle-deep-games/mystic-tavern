from django.contrib import admin
from .models import Game, GameUser, Role, Gender, Weapon, Armor, Ability, Dialogue

# Register your models here.
admin.site.register(Game)
admin.site.register(GameUser)
admin.site.register(Role)
admin.site.register(Gender)
admin.site.register(Weapon)
admin.site.register(Armor)
admin.site.register(Ability)
admin.site.register(Dialogue)
