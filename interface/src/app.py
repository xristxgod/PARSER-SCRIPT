from flask import Flask

import src.views as views
from config import Config


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(views.app)
