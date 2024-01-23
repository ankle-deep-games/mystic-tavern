from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tavern_app.urls")),
    path(
        "login/",
        CustomLoginView.as_view(
            template_name="registration/login.html", next_page="tavern_app:games"
        ),
        name="login",
    ),
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="tavern_app:home"), name="logout"),
]
