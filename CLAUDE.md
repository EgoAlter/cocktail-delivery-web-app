# CLAUDE.md — cocktail-delivery-web-app

## Project overview

A cocktail delivery web app built with Flask. Customers browse a menu, add items to a cart, check out, and receive email confirmation. Staff can view and manage orders via a dashboard.

## Tech stack

- **Python** 3.14 / **Flask** 3.1.3
- **SQLAlchemy** 2.0 via Flask-SQLAlchemy 3.1 (ORM)
- **Flask-Mail** 0.10 (transactional email)
- **Flask-Login** — not yet installed, needed for auth (add to requirements.txt when implementing)
- **Database** — SQLite locally (`sqlite:///cocktails.db`), configurable via `DATABASE_URL`
- **Frontend** — Jinja2 templates, vanilla JS, plain CSS (no framework)

## Project structure

```
run.py                  # entry point: calls create_app() and runs the dev server
app/
  __init__.py           # app factory: create_app() wires extensions + blueprints
  config.py             # Config class reads from .env
  extensions.py         # shared db and mail instances (import from here, never re-create)
  models.py             # SQLAlchemy models (empty — needs implementing)
  blueprints/
    auth.py             # login, logout, register routes
    menu.py             # browse products
    cart.py             # cart, checkout, confirmation
    dashboard.py        # staff order management
    api.py              # JSON endpoints (reserved)
  templates/            # Jinja2 HTML — mirrors blueprint names
  static/
    css/main.css
    js/cart.js, menu.js, dashboard.js
seed.py                 # populate DB with sample data (empty — implement alongside models)
```

## Known structural issue

`app/__init__.py` is currently missing — the `create_app` factory lives in `app/blueprints/__init__.py` with a comment saying it belongs at `app/__init__.py`. This means `run.py` (`from app import create_app`) will fail. **Fix before running:** move the factory to `app/__init__.py`.

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root (already gitignored):
```
SECRET_KEY=<random string>
DATABASE_URL=sqlite:///cocktails.db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=<your email>
MAIL_PASSWORD=<app password>
```

Run the dev server:
```bash
python run.py
```

## Architecture conventions

- **Factory pattern** — always use `create_app()`, never instantiate `Flask` at module level.
- **Extensions** — import `db` and `mail` from `app.extensions`, never re-create them.
- **Blueprints** — one per feature area; register them inside `create_app()` in `app/__init__.py`.
- **Models** — all in `app/models.py`; import `db` from `app.extensions`.
- **No circular imports** — blueprints import models inside route functions or at the top of the blueprint file, not at module level in `__init__.py`.

## Build status

| Area | Status |
|---|---|
| App factory + config | Done |
| Blueprint scaffold | Done (routes empty) |
| Database models | Not started |
| Auth (login/register) | Not started — needs Flask-Login |
| Menu / product listing | Not started |
| Cart + checkout | Not started |
| Staff dashboard | Not started |
| Email notifications | Not started |
| Templates | Empty stubs |
| Seed data | Empty stub |
| Tests | Empty directory |

## Suggested build order

1. Fix `app/__init__.py` placement
2. Install Flask-Login, Flask-Migrate — add to `requirements.txt`
3. Define models (`User`, `Product`, `Order`, `OrderItem`)
4. Run migrations, write seed data
5. Auth blueprint (register, login, logout)
6. Menu blueprint (list products, product detail)
7. Cart blueprint (add/remove, checkout, confirmation)
8. Dashboard blueprint (staff order list, order detail, status update)
9. Email notifications (order confirmed, order delivered)
10. Frontend polish (CSS, JS)

## GitHub

Remote: `https://github.com/EgoAlter/cocktail-delivery-web-app`
Branch strategy: feature branches → PR → merge to `main`.
