import os


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
