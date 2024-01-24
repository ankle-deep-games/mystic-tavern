from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Game, GameUser, GameDialogue, CombatLog, Role


class CreateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ("name", "password")
        error_messages = {
            'name': {
                'max_length': "Game name must be less than 17 characters.",
                'min_length': "Game name must be at least 3 characters.",
            },
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "minlength": 3}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        min_length = 3

        if len(name) < min_length:
            raise ValidationError(self.Meta.error_messages['name']['min_length'])

        return name


class JoinGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ("password",)

        widgets = {"password": forms.TextInput(attrs={"class": "form-control"})}


class StartGameForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput())


class RoleAssignmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset and label for the role field to use display_name
        self.fields['role'].queryset = Role.objects.all()
        self.fields['role'].label_from_instance = lambda obj: obj.display_name

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
