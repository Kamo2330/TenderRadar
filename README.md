# TenderRadar

Public listing of open South African tenders and RFQs.

TenderRadar is a Django website. Anyone can browse, search, and filter tenders. There is no signup and no login.

Data is compiled from public sources (eTenders and Tenders-SA). Always confirm details on the official publication before you submit a bid.

## Features

- Public tender listing at `/`
- Search by keyword
- Filter by province, type, and source
- Sort by newest or closing date
- Sample tenders for local testing
- Optional live scrape from public APIs

## Requirements

- Python 3.11 or later
- Git

## Setup

```cmd
git clone https://github.com/Kamo2330/TenderRadar.git
cd TenderRadar
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py load_sample_tenders
python manage.py runserver
```

On macOS or Linux, use `source .venv/bin/activate` and `cp .env.example .env`.

Open http://127.0.0.1:8000/

If the page looks outdated, use Incognito or press Ctrl+Shift+R.  
http://127.0.0.1:8000/health/ should show `UI: square-v7`.

## Commands

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Start the site |
| `python manage.py load_sample_tenders` | Load 12 example tenders |
| `python manage.py scrape_tenders` | Fetch live public tenders |
| `python manage.py test` | Run tests |

## Stack

Django, SQLite (local), HTML, CSS, and JavaScript.

## License

[MIT](LICENSE)
