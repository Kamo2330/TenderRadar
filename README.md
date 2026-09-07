# TenderRadar

South African tender discovery — Django app with public dashboard and scraper.

## Run locally (Windows)

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

No login required for the public tender register. Admin: http://127.0.0.1:8000/admin/

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
