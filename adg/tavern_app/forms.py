from django import forms
from django.forms import ModelForm

from .models import Game, GameUser, GameDialogue, CombatLog


class CreateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ("name", "password")

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
        }


class JoinGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ("password",)

        widgets = {"password": forms.TextInput(attrs={"class": "form-control"})}


class StartGameForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput())


class RoleAssignmentForm(ModelForm):
    class Meta:
        model = GameUser
        fields = ['role', 'gender']


class GameDialogueForm(ModelForm):
    class Meta:
        model = GameDialogue
        fields = ["dialogue"]


class CombatLogForm(ModelForm):
    class Meta:
        model = CombatLog
        fields = ["gameenemy", "ability", "defensive_gameuser_target"]
