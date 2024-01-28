from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from .models import Game, GameUser, GameDialogue, CombatLog, Role


class CreateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ("name", "password")
        labels = {
            'name': 'Name (up to 16 characters)',
        }
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


class BaseRoleAssignmentFormSet(BaseInlineFormSet):
    def clean(self):
        # TODO remove role assignments prints when done debugging
        # https://trello.com/c/9DhXpUWT/296-role-assignments-form-debug
        print("BaseRoleAssignmentFormSet CLEAN")
        """Custom formset-level validation."""
        if any(self.errors):
            print("BaseRoleAssignmentFormSet IF ANY ERRORS")
            # Don't perform validation if there are form errors already
            return

        roles = [form.cleaned_data.get('role') for form in self.forms if form.cleaned_data.get('role')]
        print("BaseRoleAssignmentFormSet ROLES")
        print(roles)
        if len(roles) != len(set(roles)):
            raise forms.ValidationError("Each player must have a unique role.")

        for form in self.forms:
            role = form.cleaned_data.get('role')
            gender = form.cleaned_data.get('gender')
            print(role)
            print(gender)

            if not role or not gender:
                raise forms.ValidationError("Every player must have a role and gender selected.")

        return super().clean()
