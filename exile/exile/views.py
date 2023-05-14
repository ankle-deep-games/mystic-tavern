from django.shortcuts import render
from django.views.generic import TemplateView


def login_user(request):
    return render(request, 'registration/login.html', {})


class CreateOrJoinView(TemplateView):
    template_name = "home.html"


class ChooseGameView(TemplateView):
    template_name = "choose_game.html"
