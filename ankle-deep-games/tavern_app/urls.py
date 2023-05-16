from django.urls import path
from . import views
from .views import GameView, GameDetailView, GameUsersView, CreateGameView

app_name = 'tavern_app'

# domain.com/tavern_app/
urlpatterns = [
    path('', views.simple_view),
    path('create_game/', CreateGameView.as_view(), name='create_game'),
    path('games/', GameView.as_view(), name='games'),
    path('games/<int:pk>', GameDetailView.as_view(), name='game_detail'),
    path('games/<int:game_id>/lobby', GameUsersView.as_view(), name='lobby'),
]
