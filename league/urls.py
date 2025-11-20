from django.urls import path
from . import views

urlpatterns = [
    path("", views.TeamListView.as_view(), name="team_list"),
    path("games/", views.GameListView.as_view(), name="game_list"),
]
