from django.contrib import admin
from .models import Game, GameUser, Role

# Register your models here.
admin.site.register(Game)
admin.site.register(GameUser)
admin.site.register(Role)
