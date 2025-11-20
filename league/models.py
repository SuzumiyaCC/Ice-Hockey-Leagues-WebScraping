from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    games_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    ot_wins = models.PositiveIntegerField(default=0)
    shootout_wins = models.PositiveIntegerField(default=0)
    shootout_losses = models.PositiveIntegerField(default=0)
    ot_losses = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    shootout_against = models.PositiveIntegerField(default=0)
    shootout = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    penalty_minutes = models.PositiveIntegerField(default=0)
    penalty_minutes_against = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["number", "name"]

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    game_date = models.DateField()
    home_team = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    venue = models.CharField(max_length=128, blank=True)
    source_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-game_date", "home_team__name"]
        unique_together = ("game_date", "home_team", "away_team")

    def __str__(self) -> str:
        return f"{self.away_team} at {self.home_team} on {self.game_date}"
