import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    environmnet_configuration = os.getenv('CONFIGURATION_SETUP')
    app.config.from_object(environmnet_configuration)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        return app