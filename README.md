# TenderRadar

South African tender register — Django only. Public dashboard at `/`.

**Use this repository on `main` only.** Old folders and old branches are outdated.

## Fresh start (Windows)

Delete every old copy first, then clone once:

```cmd
cd C:\Users\Admin\Desktop
rmdir /s /q TenderRadar
rmdir /s /q TenderRadar_LIVE
rmdir /s /q TenderRadar_NEW
git clone https://github.com/Kamo2330/TenderRadar.git TenderRadar
cd TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py load_sample_tenders
python manage.py runserver
```

Or double-click **`CLEAN_PC.bat`** then **`RUN.bat`**.

Open **http://127.0.0.1:8000/** in **Incognito**.

Check **http://127.0.0.1:8000/health/** — it must say `UI: square-v6`.

## Daily run

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
.venv\Scripts\activate
python manage.py runserver
```

## License

[MIT](LICENSE)
