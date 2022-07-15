import os


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.db')}")
    SECRET_KEY = os.environ.get("SECRET_KEY", "324bef6c5985f7ad7c8527d2")
