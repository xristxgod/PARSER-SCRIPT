from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import views
from config import Config


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.register_blueprint(views.app)


def db_setup():
    db.create_all()

