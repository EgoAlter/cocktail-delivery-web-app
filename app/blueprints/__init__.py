# app/__init__.py
# The app factory — creates and configures the Flask application.
# "Factory" pattern means we call create_app() to build the app,
# rather than creating it at module level. This makes testing easier
# and avoids circular import issues between blueprints and models.

from flask import Flask
from app.extensions import db, mail
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions — binding them to THIS app instance
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints — each one is a feature area
    # (these files are empty placeholders for now, we'll fill them later)
    from app.blueprints.auth import auth_bp
    from app.blueprints.menu import menu_bp
    from app.blueprints.cart import cart_bp
    from app.blueprints.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(dashboard_bp)

    return app