import config
import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


login_manager = LoginManager()
bootstarp = Bootstrap()
UPLOAD_FOLDER = 'application/static/images'


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "frontend.login"

    bootstarp.init_app(app)

    with app.app_context():
        return app