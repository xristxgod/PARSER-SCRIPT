from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from src import app

db = SQLAlchemy(app)


class OrderModel(db.Model):
    __tablename__ = "order_model"
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, unique=True)
    price_usd = db.Column(db.Float, default=0)
    price_rub = db.Column(db.Float, default=0)
    delivery_time = db.Column(db.DateTime, default=datetime.now().strftime("%d/%m/%Y"))

    def __repr__(self):
        return f"{self.order_id}"


def db_setup():
    db.create_all()
