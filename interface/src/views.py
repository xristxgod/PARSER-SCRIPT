from flask import Blueprint, render_template

from .models import OrderModel


app = Blueprint("main", __name__)


@app.route("/", methods=['GET', 'POST'])
def index_page():
    all_orders = OrderModel.query.all()
    return render_template("index.html", **{
        "allOrders": all_orders,
        "totalOrders": len(all_orders)
    })
