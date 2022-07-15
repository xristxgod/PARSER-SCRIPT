from flask import Flask

import views


app = Flask(__name__)
app.register_blueprint(views.app)
