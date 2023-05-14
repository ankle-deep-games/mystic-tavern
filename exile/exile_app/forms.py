from django import forms
from .models import Game


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'password')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }
