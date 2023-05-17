from django.shortcuts import render
from django.views.generic import TemplateView


def login_user(request):
    return render(request, 'registration/login.html', {})


class CreateOrJoinView(TemplateView):
    template_name = "home.html"


class ChooseGameJoinView(TemplateView):
    template_name = "choose_game_join.html"


class ChooseGameCreateView(TemplateView):
    template_name = "choose_game_create.html"
