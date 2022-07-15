from flask import Blueprint


app = Blueprint("main", __name__)


@app.route("/", methods=['GET', 'POST'])
def index_page():
    pass
