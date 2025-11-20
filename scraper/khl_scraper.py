import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khlsite.settings")
import django  # noqa: E402

django.setup()

from league.models import Game, Team  # noqa: E402

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "scraper.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

KHL_CALENDAR_URL = os.getenv("KHL_CALENDAR_URL", "https://en.khl.ru/calendar/")
FALLBACK_JSON = Path(__file__).resolve().parents[1] / "shlscraper" / "json" / "khlLeague.json"


def _parse_calendar_html(html: str) -> List[Tuple[str, str, str, str, str]]:
    """Parse a minimal game list from the public KHL calendar page.

    Returns tuples of (date, home_team, away_team, home_score, away_score).
    If a score cannot be found the tuple will contain empty strings for scores.
    """
    soup = BeautifulSoup(html, "html.parser")
    games: List[Tuple[str, str, str, str, str]] = []
    for row in soup.select("div.calendar__game"):
        date_text = row.get("data-date") or row.select_one(".calendar__date")
        date_val = date_text.get_text(strip=True) if hasattr(date_text, "get_text") else str(date_text)
        teams = row.select(".calendar__team")
        if len(teams) != 2:
            continue
        home_team = teams[0].get_text(strip=True)
        away_team = teams[1].get_text(strip=True)
        score_block = row.select_one(".calendar__score")
        home_score = away_score = ""
        if score_block:
            scores = score_block.get_text(strip=True).split(":")
            if len(scores) == 2:
                home_score, away_score = scores
        games.append((date_val, home_team, away_team, home_score, away_score))
    return games


def _load_standings_from_json() -> Iterable[dict]:
    if not FALLBACK_JSON.exists():
        logger.warning("Fallback standings file not found: %s", FALLBACK_JSON)
        return []
    with open(FALLBACK_JSON, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    for row in data.get("teamdata", [])[1:]:
        (
            name,
            number,
            games_played,
            wins,
            ot_wins,
            shootout_wins,
            shootout_losses,
            ot_losses,
            losses,
            shootout_against,
            shootout,
            goals_for,
            goals_against,
            penalty_minutes,
            penalty_minutes_against,
        ) = row
        yield {
            "name": name,
            "number": int(number),
            "games_played": int(games_played),
            "wins": int(wins),
            "ot_wins": int(ot_wins),
            "shootout_wins": int(shootout_wins),
            "shootout_losses": int(shootout_losses),
            "ot_losses": int(ot_losses),
            "losses": int(losses),
            "shootout_against": int(shootout_against),
            "shootout": int(shootout),
            "goals_for": int(goals_for),
            "goals_against": int(goals_against),
            "penalty_minutes": int(penalty_minutes),
            "penalty_minutes_against": int(penalty_minutes_against),
        }


def sync_standings() -> None:
    logger.info("Loading standings from %s", FALLBACK_JSON)
    created, updated = 0, 0
    for payload in _load_standings_from_json():
        obj, is_created = Team.objects.update_or_create(name=payload.pop("name"), defaults=payload)
        if is_created:
            created += 1
        else:
            updated += 1
    logger.info("Standings sync complete. created=%s updated=%s", created, updated)


def sync_games_from_web() -> None:
    logger.info("Fetching latest calendar from %s", KHL_CALENDAR_URL)
    try:
        response = requests.get(KHL_CALENDAR_URL, timeout=20)
        response.raise_for_status()
    except Exception as exc:  # broad catch to capture network issues in log
        logger.error("Could not download KHL calendar: %s", exc)
        return

    games = _parse_calendar_html(response.text)
    logger.info("Parsed %s games from calendar", len(games))
    for date_text, home, away, home_score, away_score in games:
        if not (date_text and home and away):
            continue
        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            # Attempt day-month-year format used on the site
            try:
                parsed_date = datetime.strptime(date_text, "%d.%m.%Y").date()
            except ValueError:
                logger.debug("Skipping unrecognized date format: %s", date_text)
                continue
        home_team, _ = Team.objects.get_or_create(name=home)
        away_team, _ = Team.objects.get_or_create(name=away)
        defaults = {}
        if home_score.isdigit() and away_score.isdigit():
            defaults.update({
                "home_score": int(home_score),
                "away_score": int(away_score),
            })
        Game.objects.update_or_create(
            game_date=parsed_date,
            home_team=home_team,
            away_team=away_team,
            defaults=defaults,
        )


if __name__ == "__main__":
    logger.info("Starting KHL scrape")
    sync_standings()
    sync_games_from_web()
    logger.info("Scrape finished")
