from flask import Blueprint

from .models import OrderModel


app = Blueprint("main", __name__)


@app.route("/", methods=['GET', 'POST'])
def index_page():
    print("Hello")
