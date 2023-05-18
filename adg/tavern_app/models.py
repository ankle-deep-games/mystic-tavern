from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Game Name: ' + str(self.name) + ', Created by: ' + str(self.creator)


class Role(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Gender(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class GameUser(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=None, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        game_name = self.game.name if self.game else 'Unknown Game'
        username = self.user.username if self.user else 'Unknown User'
        role_name = self.role.name if self.role else 'Unknown Role'

        return f'Game Name: {game_name}, Player: {username}, Role: {role_name}'
