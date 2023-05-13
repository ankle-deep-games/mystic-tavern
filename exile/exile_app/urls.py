from django.urls import path
from . import views
from .views import GameView

app_name = 'exile_app'

# domain.com/exile_app/
urlpatterns = [
    path('', views.simple_view),
    path('games', GameView.as_view(), name='games'),
]
