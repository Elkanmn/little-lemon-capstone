# Little Lemon Restaurant — Django REST API

A course-oriented Little Lemon reference implementation: Django-rendered HTML, MySQL persistence, Django REST Framework endpoints for menus and bookings, token registration/login, admin, tests, and an Insomnia collection.

> **Academic integrity:** This is an AI-generated reference project. Coursera's Honor Code shown in the assignment warns that submitting AI-created work may result in penalties. Understand and substantially implement/verify your own work, and follow your course's current rules before submitting.

## Requirements

- Python 3.10+ and pip
- Docker Desktop (recommended to run MySQL 8.4) or an existing MySQL 8+ server
- VS Code (optional), Git, and Insomnia (optional)

## Start with MySQL (recommended)

From this folder, run on macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and change `DJANGO_SECRET_KEY`, `DB_PASSWORD`, and `MYSQL_ROOT_PASSWORD` **before** starting the database. Keep `.env` private.

```bash
docker compose up -d db
# Wait until `docker compose ps` reports healthy; first launch may take time.
python manage.py migrate
python manage.py seed_menu
python manage.py createsuperuser
python manage.py test restaurant
python manage.py runserver
```

Browse `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/api/menu/`. For admin use `http://127.0.0.1:8000/admin/`. For cleanup, `docker compose down` stops the container; **do not** add `-v` unless you intend to delete database data.

### Existing MySQL instead of Docker

Create the database and dedicated user in your own MySQL installation (adapt host/port to your system):

```sql
CREATE DATABASE little_lemon_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'littlelemon'@'localhost' IDENTIFIED BY 'YOUR_PRIVATE_PASSWORD';
GRANT ALL PRIVILEGES ON little_lemon_db.* TO 'littlelemon'@'localhost';
```

Update `DB_HOST`, `DB_PORT`, `DB_USER`, and `DB_PASSWORD` in `.env` to match. A MySQL host connecting via TCP 127.0.0.1 may require a matching `'littlelemon'@'127.0.0.1'` account depending on MySQL server configuration. The default Docker setup uses port 3307 and manages account creation automatically.

### SQLite-only sanity check (not a substitute for MySQL grading)

If MySQL or Docker is unavailable, you can run a temporary local development check:

```bash
DB_ENGINE=sqlite python manage.py migrate
DB_ENGINE=sqlite python manage.py seed_menu
DB_ENGINE=sqlite python manage.py test restaurant
DB_ENGINE=sqlite python manage.py runserver
```

**Switch back to MySQL and rerun the tests before submitting** — the rubric asks for MySQL connectivity.

## API quick reference

Full endpoint paths and payloads are in [Readme.txt](Readme.txt), as requested by the course. Requests to the booking API require a token. The menu is publicly readable; only staff can edit it.

| Method | Endpoint | Access |
| --- | --- | --- |
| GET | `/` | Public HTML |
| GET | `/api/menu/` | Public |
| GET | `/api/menu/1/` | Public |
| POST/PUT/PATCH/DELETE | `/api/menu/` or `/api/menu/1/` | Staff |
| POST | `/api/registration/` | Public |
| POST | `/api/token/` | Public |
| POST | `/api/logout/` | Logged-in |
| GET/POST | `/api/bookings/` | Logged-in |
| GET/PUT/PATCH/DELETE | `/api/bookings/1/` | Owner or staff |

Aliases are also provided at `/restaurant/menu/` and `/restaurant/booking/tables/` to mirror wording common in the assignment.

### Example: register and book

```bash
curl -X POST http://127.0.0.1:8000/api/registration/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"student1","email":"student1@example.com","password":"SecurePass479!"}'
```

Copy the `token` field from the response. Then make a booking with a **future** date:

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Token REPLACE_WITH_YOUR_TOKEN' \
  -d '{"name":"Amina","email":"amina@example.com","no_of_guests":4,"booking_date":"2027-02-12","booking_time":"19:30:00"}'
```

If the example date has passed, replace it with a future date.

For `POST /api/menu/`, log in with a staff user created via `createsuperuser` and obtain the staff user's token using `POST /api/token/`.

### Insomnia

Import `insomnia/LittleLemon_Insomnia.json` into Insomnia. The base environment contains `base_url`, `token`, `menu_id`, and `booking_id`. After registering, paste your token into the `token` environment variable. Keep personal tokens private.

### Automated tests

```bash
python manage.py test restaurant --verbosity 2
```

The tests cover the HTML home, health, public menu access, staff-only menu changes, registration/token flow, logout, owner-isolated booking CRUD, validation, and aliases. Tests run against the currently configured DB engine.

### Security and limitations

- This project is a **learning implementation**, not production-ready. DEBUG and secrets must be set securely for real deployment.
- Do not publicly publish `.env`, passwords, live tokens, `db.sqlite3`, or private customer information.
- Booking ownership is enforced on the server; non-staff users cannot access other users' bookings.
- This demo does not handle payment, email confirmations, table inventory, or time-slot collision prevention.
- HTML is a styled static home page served with Django templates; menu CRUD and bookings are provided by the JSON API.

## GitHub / peer review

After checking your own implementation and course policy:

```bash
git init
git add .
git commit -m "Implement Little Lemon Django capstone"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Create the empty GitHub repo first, and replace the remote URL with your own URL. Before pushing, check `git status` and `git diff --cached --name-only` to ensure `.env` was excluded. In Coursera's **My submission** enter your project title and real public GitHub URL, preview, and submit only if you comply with the Honor Code. Afterwards review two peers.
