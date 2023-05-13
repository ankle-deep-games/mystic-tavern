from django.urls import path
from . import views
from .views import GameView, GameDetailView

app_name = 'exile_app'

# domain.com/exile_app/
urlpatterns = [
    path('', views.simple_view),
    path('games', GameView.as_view(), name='games'),
    path('games/<int:pk>', GameDetailView.as_view(), name='game_detail'),
]
