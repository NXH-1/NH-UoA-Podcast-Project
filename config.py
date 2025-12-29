"""Flask configuration variables."""
from os import environ, urandom
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # random key each time so each start of app, the users won't be saved from previous sessions
    SECRET_KEY = urandom(24)

    TESTING = environ.get('TESTING')

    REPOSITORY = environ.get('REPOSITORY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    echo_string = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo_string:
        SQLALCHEMY_ECHO = True
