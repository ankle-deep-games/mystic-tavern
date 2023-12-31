from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tavern_app.urls")),
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html", next_page="tavern_app:games"
        ),
        name="login",
    ),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page="tavern_app:home"), name='logout'),
]
