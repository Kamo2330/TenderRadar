# Desktop setup (ignore Git — just run the app)

Use the folder on your Desktop: `C:\Users\Admin\Desktop\TenderRadar`

## Step 1 — Cancel the broken Git merge (run once)

Open **Command Prompt**:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
git merge --abort
git fetch origin
git reset --hard origin/main
```

This wipes merge conflicts and matches your Desktop folder to the working version on GitHub (includes signup). Your old `db.sqlite3` may be removed — run setup again to recreate it.

**After this, you can ignore Git** and just edit files on Desktop.

## Step 2 — Backend

Double-click **`setup.bat`** in the TenderRadar folder, or:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar
setup.bat
python manage.py createsuperuser
python manage.py runserver
```

## Step 3 — Frontend (optional)

Double-click **`frontend\setup.bat`**, or:

```cmd
cd C:\Users\Admin\Desktop\TenderRadar\frontend
setup.bat
npm run dev
```

## Signup URLs

| Django | http://127.0.0.1:8000/accounts/signup/ |
| Next.js | http://localhost:3000/signup |

## No Git needed after Step 1

Just edit files in `C:\Users\Admin\Desktop\TenderRadar` and restart the servers when you change code.
