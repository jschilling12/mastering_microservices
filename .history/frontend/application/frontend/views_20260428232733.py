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

@frontend_blueprint.route('/product/<slug>', methods=['GET'])
def product(slug):
    response = ProductClient.get_product(slug)
    item = response['result']

    form = forms.ItemForm(product_id=item['id'])
    if request.method == 'POST':
        if 'user' not in session:
            flash("Please login to add items to your cart", 'error')
            return redirect(url_for('frontend.login'))
        order = OrderClient.post_add_to_cart(product_id=item['id'], qty=1) 
        session['order'] = order['results']
        flash("Item added to cart", 'success')
    return render_template('product/index.html', product=item, form=form)

@frontend_blueprint.route('/checkout', methods=['GET', 'POST'])
def summary():
    if 'user' not in session:
        flash("Please login to checkout", 'error')
        return redirect(url_for('frontend.login'))
    order = OrderClient.post_checkout()
    session['order'] = order['results']
    flash("Checkout successful", 'success')
    return render_template('checkout/index.html', order=order['results'])


