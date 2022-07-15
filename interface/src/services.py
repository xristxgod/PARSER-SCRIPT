import datetime
from typing import Tuple, List

from src.settings import db
from src.models import OrderModel


def get_orders(currency: str = "USD") -> List[Tuple[float, datetime.datetime]]:
    try:
        return db.session.query(
            OrderModel.price_usd if currency == "USD" else OrderModel.price_rub,
            OrderModel.delivery_time
        ).order_by(
            OrderModel.delivery_time
        ).all()
    except Exception:
        return []


def get_statistic_data(currency: str = "USD") -> Tuple[List, List]:
    """Get data for create diagram"""
    orders = get_orders(currency=currency)
    if orders is not None and len(orders) > 0:
        all_dates = []
        all_price = []
        for amount, date in orders:
            all_dates.append(date.strftime("%m-%d-%y"))
            all_price.append(amount)
        return all_dates, all_price
    return [], []
