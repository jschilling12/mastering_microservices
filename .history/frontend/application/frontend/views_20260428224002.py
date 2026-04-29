import requests
from . import forms
from . import frontend_blueprint
from .. import login_manager
from .api.UserClient import UserClient
from .api.ProductClient import ProductClient
from .api.OrderClient import OrderClient
from flask import render_template, redirect, url_for, session, flash, request

from flask_login import current_user

@login_manager.user_loader
def load_user(api_key):
    return None

@frontend_blueprint.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()
    try:
        products = ProductClient.get_products()
    except requests.exceptions.ConnectionError:
        products = {
            'results': []
        }
    return render_template('home/index.html', products=products)