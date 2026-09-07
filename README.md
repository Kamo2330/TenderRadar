# TenderRadar

South African tender discovery — Django app with public dashboard and scraper.

Browse open tenders at `/`. Staff tools and admin live under `/admin/` and `/staff/`.

## Quick start (Windows)

```cmd
git clone https://github.com/Kamo2330/TenderRadar.git
cd TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
```

Double-click **`RUN.bat`** or:

```cmd
python manage.py runserver 8765
```

Open http://127.0.0.1:8765/ — no login required for the public dashboard.

Use **`VERIFY.bat`** to confirm the server responds (avoids browser cache issues on port 8000).

## Load tender data

```cmd
python manage.py scrape_tenders
```

## Run tests

```cmd
python manage.py test
```

## License

[MIT](LICENSE)
