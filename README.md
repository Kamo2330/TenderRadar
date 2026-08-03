# TenderRadar

South African tender discovery platform — Django REST API + Next.js frontend.

---

## Windows setup (copy-paste into Command Prompt)

**Important:** The project folder is on your **Desktop**, not in `C:\Users\Admin`.

Open **Command Prompt** and run these commands **one at a time** (do not copy lines starting with `REM`):

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
```

If that fails, find where you cloned/downloaded the repo. Common paths:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
cd C:\Users\Admin\Documents\GitHub\TenderRadar
dir C:\Users\Admin\Desktop
```

### Backend (Django)

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Leave that terminal open. API runs at http://127.0.0.1:8000/

### Frontend (Next.js) — open a **second** Command Prompt

```cmd
cd C:\Users\Admin\Desktop\TenderRadar\frontend
copy .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 and sign in with your superuser account.

### Load tender data (third terminal, optional)

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
.venv\Scripts\activate
python manage.py scrape_tenders
```

---

## If you don't have the latest code yet

Pull from GitHub first:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
git pull origin cursor/portfolio-setup-7dd3
```

Or clone fresh:

```cmd
cd C:\Users\Admin\Desktop
git clone https://github.com/Kamo2330/TenderRadar.git
cd TenderRadar
git checkout cursor/portfolio-setup-7dd3
```

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | Django 6, Django REST Framework |
| Database | SQLite (local), PostgreSQL (production) |

---

## Environment variables

Copy `.env.example` to `.env` (backend) and `frontend\.env.local.example` to `frontend\.env.local`.

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret (change in production) |
| `DEBUG` | `True` for local dev |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` |
| `NEXT_PUBLIC_API_URL` | `http://127.0.0.1:8000/api` |

---

## Run tests

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
.venv\Scripts\activate
python manage.py test
```

---

## License

[MIT](LICENSE)
