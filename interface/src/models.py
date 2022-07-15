from datetime import datetime

from .app import db


class UserModel(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, unique=True)
    price_usd = db.Column(db.Float, default=0)
    price_rub = db.Column(db.Float, default=0)
    delivery_time = db.Column(db.DateTime, default=datetime.now().strftime("%d/%m/%Y"))

    def __repr__(self):
        return f"{self.order_id}"
