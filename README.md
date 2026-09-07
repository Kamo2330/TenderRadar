# TenderRadar

South African tender listing — Django app. Open tenders at `/`. No login.

## Run (Windows)

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py load_sample_tenders
python manage.py runserver
```

Open http://127.0.0.1:8000/ in Incognito.

Health check: http://127.0.0.1:8000/health/ must say `UI: square-v7`.

## Load live tenders

```cmd
python manage.py scrape_tenders
```

## License

[MIT](LICENSE)
