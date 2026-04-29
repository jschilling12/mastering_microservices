import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = "2wRUamkrkUwLpfsa4k00Cw"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    ENV='development'
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cloudacademy:pfm_2020@localhost:3306/user_dev'
    # Docker containter SQL access
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cloudacademy:pfm_2020@host.docker.interal:3306/user_dev'
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass


