from django.urls import path
from . import views
from .views import GameView, GameDetailView, GameUsersView, CreateGameView, RoleAssignmentView, Act1Scene1View

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
    path('games/<int:game_id>/act1/scene1', views.act1_scene1_view, name='act1_scene1'),
    path('liveupdateprototype', views.live_update_prototype, name='liveupdateprototype'),
    path('liveupdateprototypeview', views.live_update_prototype_view, name='liveupdateprototypeview'),
    path('liveupdateprototyperedirectview', views.live_update_prototype_redirect_view, name='liveupdateprototyperedirectview'),
]
