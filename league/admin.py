from django.contrib import admin
from .models import Team, Game


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "number",
        "games_played",
        "wins",
        "losses",
        "ot_wins",
        "ot_losses",
    )
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("game_date", "home_team", "away_team", "home_score", "away_score")
    search_fields = ("home_team__name", "away_team__name")
    list_filter = ("game_date",)
