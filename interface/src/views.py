import json
from flask import Blueprint, render_template

from .settings import db
from .models import OrderModel
from .services import get_statistic_data


app = Blueprint("main", __name__)


@app.route("/", methods=['GET', 'POST'])
def index_page():
    all_dates_usd, all_price_usd = get_statistic_data()
    return render_template("index.html", **{
        "all_price_usd": json.dumps(all_price_usd, default=str),
        "all_dates_usd": json.dumps(all_dates_usd),
        "totalOrders": len(all_price_usd)
    })
