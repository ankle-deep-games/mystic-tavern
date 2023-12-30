from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
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
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
