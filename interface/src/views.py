import json
import math
from flask import Blueprint, render_template

from .settings import db
from .models import OrderModel
from .services import get_statistic_data


app = Blueprint("main", __name__)


@app.route("/", methods=['GET', 'POST'])
def index_page():
    """Main page"""
    orders = OrderModel.query.all()
    all_dates_usd, all_price_usd = get_statistic_data(currency="USD")
    all_dates_rub, all_price_rub = get_statistic_data(currency="RUB")
    return render_template("index.html", **{
        "orders": orders,
        "all_price_usd": json.dumps(all_price_usd, default=str),
        "all_dates_usd": json.dumps(all_dates_usd),
        "total_orders": len(orders),
        "total_orders_price_usd": round(math.fsum(all_price_usd), 3),
        "total_orders_price_rub": round(math.fsum(all_price_rub), 3)
    })
