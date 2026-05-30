# Cocktail Delivery

A full-stack cocktail delivery web app built with Flask. Customers browse a menu, add items to a cart, check out, and receive email confirmation. Staff manage and update orders via a dashboard.

**Live demo:** [YOUR-APP-URL]

---

## Features

- Browse a menu of cocktails with category tags and pricing
- Add items to a session-based cart, update quantities, remove items
- Checkout with a delivery address — order saved to database
- Email notifications: order confirmed on checkout, delivery notification when staff marks delivered
- Staff dashboard: view all orders, filter by status, update order status
- User registration and login with secure password hashing
- Responsive dark-themed UI

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3 / Flask 3 |
| Database | MySQL (production) / SQLite (local dev) |
| ORM | SQLAlchemy 2 via Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Auth | Flask-Login |
| Email | Flask-Mail |
| Server | Gunicorn |

## Local setup

```bash
git clone https://github.com/EgoAlter/cocktail-delivery-web-app
cd cocktail-delivery-web-app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=any-random-string
DATABASE_URL=sqlite:///cocktails.db
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
```

Run migrations and seed sample data:

```bash
flask --app run:app db upgrade
python seed.py
```

Start the dev server:

```bash
python run.py
```

App runs at `http://127.0.0.1:5000`

## Demo credentials

| Role | Email | Password |
|---|---|---|
| Staff | admin@cocktails.com | admin1234 |

Register any email to create a customer account.

## Project structure

```
app/
  blueprints/     # auth, menu, cart, dashboard, api
  templates/      # Jinja2 HTML templates
  static/         # CSS and JS
  models.py       # User, Product, Order, OrderItem
  email.py        # transactional email helpers
  extensions.py   # db, mail, login_manager, migrate
  config.py       # Config class reads from .env
run.py            # app entry point
seed.py           # populates DB with sample cocktails
```

## License

MIT
