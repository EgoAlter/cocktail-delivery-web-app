from flask import Flask
from app.extensions import db, mail, login_manager, migrate
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from . import models  # noqa: F401 — registers models with SQLAlchemy metadata

    from app.blueprints.auth import auth_bp
    from app.blueprints.menu import menu_bp
    from app.blueprints.cart import cart_bp
    from app.blueprints.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(dashboard_bp)

    return app
