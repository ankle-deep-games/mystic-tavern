from django import forms
from .models import Game, GameUser, Role


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'password')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }


class JoinGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('password',)

        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }


class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = GameUser
        fields = []

    def __init__(self, game_id, *args, **kwargs):
        num_players = kwargs.pop('num_players', 0)
        super().__init__(*args, **kwargs)

        players = GameUser.objects.filter(game_id=game_id)
        roles = Role.objects.all()

        for i, player in enumerate(players, start=1):
            self.fields[f'player_{i}_name'] = forms.ChoiceField(
                choices=[(player.user.username, player.user.username) for player in players], label=f'Player {i} Name')
            self.fields[f'player_{i}_role'] = forms.ModelChoiceField(queryset=roles, empty_label=None,
                                                                     label=f'Player {i} Role')

        self.Meta.fields = list(self.fields.keys())
        self.initial['num_players'] = num_players
