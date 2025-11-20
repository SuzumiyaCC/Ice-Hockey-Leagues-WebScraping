# Ice-Hockey-Leagues-WebScraping

## Django dashboard for KHL parsing
The project now ships with a lightweight Django site to view collected KHL standings and games, plus a dedicated scraper script that can run inside Docker alongside PostgreSQL.

### Running with Docker Compose
1. Build and start the stack:
   ```bash
   docker-compose up --build
   ```
   The web UI will be available on http://localhost:8000 and PostgreSQL on port 5432.

2. The `entrypoint.sh` script runs migrations and collects static assets before starting Gunicorn.

### Scraper
- The scraper lives in `scraper/khl_scraper.py` and writes detailed logs to `scraper/logs/scraper.log`.
- By default it loads fallback standings from `shlscraper/json/khlLeague.json` and attempts to fetch live games from `https://en.khl.ru/calendar/`.
- Run it inside the web container (after the stack is up) to populate the database:
  ```bash
  docker-compose exec web python scraper/khl_scraper.py
  ```

### Local development without Docker
Set `USE_SQLITE_FALLBACK=True` to use SQLite locally:
```bash
USE_SQLITE_FALLBACK=True python manage.py migrate
USE_SQLITE_FALLBACK=True python manage.py runserver
```

### Legacy Scrapy spiders
The historical Scrapy spiders remain in `shlscraper/shlscraper/spiders/` for reference but are not invoked by the new Django dashboard.
