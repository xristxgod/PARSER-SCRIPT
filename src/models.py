import datetime

import sqlalchemy
from sqlalchemy import Column, orm
from sqlalchemy.types import BigInteger, DateTime, Float

from .utils import Utils
from config import Config


BaseModel = orm.declarative_base()
engine = sqlalchemy.create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})
session = orm.Session(engine)


class OrderModel(BaseModel):
    __tablename__ = "order_model"
    id = Column(BigInteger, primary_key=True, unique=True)
    order_id = Column(BigInteger, unique=True)
    price_usd = Column(Float, default=0)
    price_rub = Column(Float, default=0)
    delivery_time = Column(DateTime, default=Utils.get_time_now())

    def __repr__(self):
        return f"{self.order_id}"
