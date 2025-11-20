from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True)),
                ("number", models.PositiveIntegerField(blank=True, null=True)),
                ("games_played", models.PositiveIntegerField(default=0)),
                ("wins", models.PositiveIntegerField(default=0)),
                ("ot_wins", models.PositiveIntegerField(default=0)),
                ("shootout_wins", models.PositiveIntegerField(default=0)),
                ("shootout_losses", models.PositiveIntegerField(default=0)),
                ("ot_losses", models.PositiveIntegerField(default=0)),
                ("losses", models.PositiveIntegerField(default=0)),
                ("shootout_against", models.PositiveIntegerField(default=0)),
                ("shootout", models.PositiveIntegerField(default=0)),
                ("goals_for", models.PositiveIntegerField(default=0)),
                ("goals_against", models.PositiveIntegerField(default=0)),
                ("penalty_minutes", models.PositiveIntegerField(default=0)),
                ("penalty_minutes_against", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["number", "name"],
            },
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("game_date", models.DateField()),
                ("home_score", models.PositiveIntegerField(default=0)),
                ("away_score", models.PositiveIntegerField(default=0)),
                ("venue", models.CharField(blank=True, max_length=128)),
                ("source_url", models.URLField(blank=True)),
                (
                    "away_team",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="away_games", to="league.team"),
                ),
                (
                    "home_team",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="home_games", to="league.team"),
                ),
            ],
            options={
                "ordering": ["-game_date", "home_team__name"],
                "unique_together": {("game_date", "home_team", "away_team")},
            },
        ),
    ]
