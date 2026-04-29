import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = "i7uB-p-pMfKUt65ogniEjx4JCuSr6w"
    WTF_CSRF_SECRET_KEY = "fG4yDq6MH2HHVUY2BomO3UAAvrUdiKAPjKxS2_sV"

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    pass