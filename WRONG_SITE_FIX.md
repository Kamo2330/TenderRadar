# Wrong site showing? (2nd Bantu / login page instead of TenderRadar)

Your server logs prove the **Desktop folder is old code**:

| Your PC (wrong) | GitHub TenderRadar (correct) |
|-----------------|------------------------------|
| Django **5.2.17** | Django **6** |
| `/` → redirect to **login** | `/` → **public tender dashboard** |
| No `static/css/tenderradar.css` | Has new CSS/JS UI |

The `/portfolio/` and `/sw.js` requests are from a **cached browser app** (likely your 2nd Bantu portfolio PWA) — not from TenderRadar.

---

## Fix in 3 steps

### 1. Reset the folder

Double-click **`fix-desktop.bat`** in `C:\Users\Admin\Desktop\TenderRadar`

Or in Command Prompt:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
git fetch origin
git reset --hard origin/main
pip install -r requirements.txt
```

### 2. Verify (optional)

Double-click **`verify.bat`** — all lines should say `[OK]`.

### 3. Run with a clean browser

```cmd
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in an **Incognito / InPrivate** window.

Do not use an old bookmark. If you still see 2nd Bantu:

- Chrome: Settings → Privacy → Clear browsing data → Cached images
- Or unregister service workers: DevTools (F12) → Application → Service Workers → Unregister

---

## Still wrong? Clone fresh

```cmd
cd C:\Users\Admin\Desktop
ren TenderRadar TenderRadar_backup
git clone https://github.com/Kamo2330/TenderRadar.git
cd TenderRadar
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate --fake-initial
python manage.py runserver
```

---

## What you should see

- Navy/gold header: **TenderRadar — SA Tender Discovery**
- Hero: **Find tenders & RFQs across South Africa**
- Search filters and tender cards
- **No login page**
