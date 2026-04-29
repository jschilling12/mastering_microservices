import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
   SQLALCHEMY_DATABASE_URI = False

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://cloudacademy:pfm_2020@localhost:3306/product_dev'

class ProductionConfig(Config):
    pass