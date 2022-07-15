from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


class Settings(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
