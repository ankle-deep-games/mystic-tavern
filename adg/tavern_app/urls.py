from django.urls import path
from . import views
from .views import GameView, GameDetailView, GameUsersView, CreateGameView, RoleAssignmentView

app_name = 'tavern_app'

# domain.com/tavern_app/
urlpatterns = [
    path('leeroy/og', views.simple_view),
    path('leeroy/new', views.leeroy),
    path('create/', CreateGameView.as_view(), name='create_game'),
    path('games/', GameView.as_view(), name='games'),
    path('games/<int:pk>', GameDetailView.as_view(), name='game_detail'),
    path('games/<int:game_id>/lobby', GameUsersView.as_view(), name='lobby'),
    path('games/<int:game_id>/lobby/role_assignment', RoleAssignmentView.as_view(), name='role_assignment'),
    path('games/<int:game_id>/lobby/customize_character', RoleAssignmentView.as_view(), name='customize_character'),
]
