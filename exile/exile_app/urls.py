from django.urls import path
from . import views

# domain.com/exile_app/
urlpatterns = [
    path('', views.simple_view)
]