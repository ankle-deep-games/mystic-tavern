from django.urls import path
from . import views
from .views import CreateOrJoinView, CreateGameView, RoleAssignmentView

app_name = 'tavern_app'

# domain.com/
urlpatterns = [
    path('home/', CreateOrJoinView.as_view(), name='home'),
    path('leeroy/og', views.simple_view),
    path('seed/', views.seed),
    path('create/', CreateGameView.as_view(), name='create_game'),
    path('games/', views.games, name='games'),
    path('games/<int:pk>', views.join_game, name='join_game'),
    path('games/<int:game_id>/lobby', views.lobby, name='lobby'),
    path('games/<int:game_id>/lobby/role_assignment', RoleAssignmentView.as_view(), name='role_assignment'),
    path('games/<int:game_id>/act/<int:act>/scene/<int:number>', views.scene, name='scene'),
    path('games/<int:game_id>/act/<int:act>/battle/<int:number>', views.battle, name='battle'),
    path('liveupdateprototype', views.live_update_prototype, name='liveupdateprototype'),
    path('liveupdateprototypeview', views.live_update_prototype_view, name='liveupdateprototypeview'),
    path('liveupdateprototyperedirectview', views.live_update_prototype_redirect_view, name='liveupdateprototyperedirectview'),
]
