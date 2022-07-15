from flask import Flask

from .views import app as route_view
from .settings import Settings, db


def init_app(config_file=Settings):
    app = Flask(__name__)
    app.config.from_object(config_file)
    db.init_app(app)
    app.register_blueprint(route_view)
    return app
