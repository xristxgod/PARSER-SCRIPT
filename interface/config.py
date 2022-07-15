import os


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.db')}")
