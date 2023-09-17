from django import forms
from django.forms import ModelForm
from .models import Game, GameUser, Role, Gender, GameDialogue, CombatLog


class CreateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'password')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }


class JoinGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ('password',)

        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }

class StartGameForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput())

class RoleAssignmentForm(ModelForm):
    class Meta:
        model = GameUser
        fields = []

    def __init__(self, game_id, *args, **kwargs):
        num_players = kwargs.pop('num_players', 0)
        super().__init__(*args, **kwargs)

        players = GameUser.objects.filter(game_id=game_id)
        roles = Role.objects.all()
        genders = Gender.objects.all()

        for i, player in enumerate(players, start=1):
            self.fields[f'player_{i}_name'] = forms.ChoiceField(
                choices=[(player.name(), player.name()) for player in players],
                label=f'Player {i} Name')
            self.fields[f'player_{i}_role'] = forms.ModelChoiceField(queryset=roles,
                                                                     empty_label=None,
                                                                     label=f'Player {i} Role')
            self.fields[f'player_{i}_gender'] = forms.ModelChoiceField(queryset=genders,
                                                                       empty_label=None,
                                                                       label=f'Player {i} Gender')

            self.initial[f'player_{i}_name'] = player.name()
            self.initial[f'player_{i}_role'] = player.role.id if player.role else None
            self.initial[f'player_{i}_gender'] = player.gender.id if player.gender else None

        self.Meta.fields = list(self.fields.keys())
        self.initial['num_players'] = num_players


class GameDialogueForm(ModelForm):
    class Meta:
        model = GameDialogue
        fields = ['dialogue']
        
class CombatLogForm(ModelForm):
    class Meta:
        model = CombatLog
        fields = ['gameenemy', 'ability', 'defensive_gameuser_target']
