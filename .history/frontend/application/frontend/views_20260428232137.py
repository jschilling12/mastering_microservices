import requests
from sqlalchemy import false
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

@frontend_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            user = UserClient.does_exist(username)
            if user:
                flash("Please try a different username", 'error')
                return render_template('register/index.html', form=form)
            else:
                user = UserClient.post_user_create(form)
                if user:
                    flash("Registration successful, please login", 'success')
                    return redirect(url_for('frontend.login'))
        else:
            flash("An error occurred, please try again", 'error')
    return render_template('register/index.html', form=form)

@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.post_login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['results']

                order = OrderClient.get_order()
                if order.get('results', false):
                    session['order'] = order['results']
                
                flash('Welcome back, ' + user['results']['username'], 'success')
                return redirect(url_for('frontend.home'))
            else:
                flash("Cannot login, please check your credentials and try again", 'error')
        else:
            flash("Errors found", "error")
    return render_template('login/index.html', form=form)

@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('frontend.home'))
