from django.views.generic import ListView
from .models import Team, Game


class TeamListView(ListView):
    model = Team
    template_name = "league/team_list.html"
    context_object_name = "teams"


class GameListView(ListView):
    model = Game
    template_name = "league/game_list.html"
    context_object_name = "games"
    paginate_by = 20
