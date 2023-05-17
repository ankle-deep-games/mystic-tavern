from django.contrib import admin
from .models import Game, GameUser, Role, Gender

# Register your models here.
admin.site.register(Game)
admin.site.register(GameUser)
admin.site.register(Role)
admin.site.register(Gender)
