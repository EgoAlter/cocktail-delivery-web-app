import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file into environment variables

class Config:
    SECRET_KEY          = os.environ.get('SECRET_KEY', 'dev-fallback-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER         = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT           = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS        = True
    MAIL_USERNAME       = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD       = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', 'noreply@cocktaildelivery.com')

    # Render (and Heroku) provide postgres:// but SQLAlchemy 2.0 requires postgresql://
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///cocktails.db')
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgres://', 'postgresql://', 1)