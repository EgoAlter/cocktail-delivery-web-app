# CLAUDE.md — cocktail-delivery-web-app

## Project overview

A cocktail delivery web app built with Flask. Customers browse a menu, add items to a cart, check out, and receive email confirmation. Staff can view and manage orders via a dashboard.

**Live:** https://egoalter.pythonanywhere.com/

## Tech stack

- **Python** 3.14 / **Flask** 3.1.3
- **SQLAlchemy** 2.0 via Flask-SQLAlchemy 3.1 (ORM)
- **Flask-Migrate** (Alembic) for database migrations
- **Flask-Login** for auth
- **Flask-Mail** for transactional email (Mailtrap for testing)
- **Database** — SQLite everywhere (local dev and PythonAnywhere production)
- **Frontend** — Jinja2 templates, vanilla JS, plain CSS (no framework)
- **Hosting** — PythonAnywhere (free tier)

## Project structure

```
run.py                  # entry point: calls create_app() and runs the dev server
app/
  __init__.py           # app factory: create_app() wires extensions + blueprints
  config.py             # Config class reads from .env
  extensions.py         # shared db, mail, login_manager, migrate instances
  models.py             # User, Product, Order, OrderItem
  email.py              # send_order_confirmed / send_order_delivered
  blueprints/
    auth.py             # register, login, logout
    menu.py             # home page / product listing
    cart.py             # add, remove, update, checkout, confirmation
    dashboard.py        # staff order list, detail, status update
    api.py              # JSON endpoints (reserved for future use)
  templates/            # Jinja2 HTML — mirrors blueprint names + emails/
  static/
    css/main.css        # dark theme, all styles
    js/                 # cart.js, menu.js, dashboard.js (reserved)
seed.py                 # populates DB with 6 cocktails + 1 staff user
migrations/             # Alembic migration files
```

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root (gitignored):
```
SECRET_KEY=<random string>
DATABASE_URL=sqlite:///cocktails.db
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=<mailtrap username>
MAIL_PASSWORD=<mailtrap password>
```

```bash
flask --app run:app db upgrade
python seed.py
python run.py
```

Staff login: `admin@cocktails.com` / `admin1234`

## Architecture conventions

- **Factory pattern** — always use `create_app()`, never instantiate `Flask` at module level.
- **Extensions** — import `db`, `mail`, `login_manager`, `migrate` from `app.extensions`.
- **Blueprints** — one per feature area; all registered inside `create_app()` in `app/__init__.py`.
- **Models** — all in `app/models.py`; `db` imported from `app.extensions`.
- **Email** — use `send_order_confirmed(order)` / `send_order_delivered(order)` from `app.email`. Failures are caught and logged — never crash the request.
- **Cart** — session-based (`session['cart']`), not stored in DB until checkout.
- **staff_required** — decorator in `dashboard.py`, returns 403 for non-staff.

## Build status

| Area | Status |
|---|---|
| App factory + config | Done |
| Database models (User, Product, Order, OrderItem) | Done |
| Migrations | Done |
| Auth (register, login, logout) | Done |
| Menu / product listing | Done |
| Cart (add, remove, update, checkout, confirmation) | Done |
| Staff dashboard (order list, detail, status update) | Done |
| Email notifications (confirmed + delivered) | Done |
| CSS / dark theme | Done |
| Seed data | Done |
| Deployed to PythonAnywhere | Done |
| Tests | Not started |

## Deployment (PythonAnywhere)

WSGI file at `/var/www/egoalter_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

path = '/home/EgoAlter/cocktail-delivery-web-app'
if path not in sys.path:
    sys.path.insert(0, path)

from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

from run import app as application
```

Virtualenv set in Web tab to the `cocktail-env` virtualenv path.

To redeploy after changes: `git pull` in PythonAnywhere console → Web tab → Reload.

## GitHub

Remote: `https://github.com/EgoAlter/cocktail-delivery-web-app`
