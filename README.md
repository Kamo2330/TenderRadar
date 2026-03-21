# TenderRadar

TenderRadar is a Django-based platform that helps businesses discover new tenders and RFQs quickly and receive alerts based on their interests.

## What it does

- **Ingests tenders from real sources**: National Treasury **OCDS API** (`ocds-api.etenders.gov.za`) and **Tenders-SA** JSON API (aggregator RFQs, including many corporate/SOE notices).
- **Normalizes data** into a `Tender` model.
- **Lets users sign up and log in**.
- **Provides a dashboard** of recent tenders.
- **Allows businesses to define alert preferences** (keywords, departments, provinces, channels).
- **Sends alerts by email** (console backend in development).

## Tech stack

- Python 3.13+
- Django 6
- SQLite (development)

## Getting started (development)

From the project root (`TenderRadar/` where `manage.py` lives):

```bash
python -m venv .venv
.venv\Scripts\activate      # On Windows PowerShell: .venv\Scripts\Activate.ps1

pip install "django>=6,<7"

python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`:

- `Log in` (accounts are created by staff; there is no public self‑signup).
- Use the **dashboard** as the main entry point.

## Testing the tender flow

1. Log in at `http://127.0.0.1:8000/accounts/login/`.
2. In another terminal, run (defaults: last **14 days** of OCDS + Tenders‑SA pages):

   ```bash
   python manage.py scrape_tenders
   ```

   Options:

   ```bash
   python manage.py scrape_tenders --source etenders --days 7
   python manage.py scrape_tenders --source tenders_sa --tsa-max-pages 5
   ```

3. New rows trigger **email alerts** (console backend in dev — printed in the terminal).

## Key apps and files

- `tenders/`
  - `models.py` – `Source`, `Tender`, `BusinessProfile`, `AlertPreference`, `AlertEvent`.
  - `views.py` – signup, dashboard, preferences, logout.
  - `services.py` – matching logic and email alert sending.
  - `templates/tenders/` – `dashboard.html`, `preferences.html`.
- `scraper/`
  - `base.py` – base scraper class.
  - `etenders.py` – demo scraper implementation.
  - `management/commands/scrape_tenders.py` – `python manage.py scrape_tenders`.
- `templates/`
  - `base.html` – Bootstrap layout and navbar.
  - `registration/login.html`, `registration/signup.html`, `registration/logged_out.html`.

## Next steps / roadmap

- Add real scrapers for:
  - National eTenders portal.
  - Gauteng municipalities.
  - Departments: Social Development, Health, etc.
  - Private sector portals and mines.
- Integrate **Telegram** and **WhatsApp** alerts.
- Add **Celery + Redis** for scheduled scraping and background alert delivery.
- Harden auth and password policies for production.

