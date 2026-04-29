import config
import os
from flask import Flask
from flask_login import LoginManager
"""
App factory for the frontend service.

Note: Removed the optional Flask-Bootstrap extension since templates already
load Bootstrap from a CDN. This avoids requiring the deprecated
`flask_bootstrap` package.
"""


login_manager = LoginManager()
UPLOAD_FOLDER = 'application/static/images'


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "frontend.login"


    with app.app_context():
        from .frontend import frontend_blueprint
        app.register_blueprint(frontend_blueprint)
        return app