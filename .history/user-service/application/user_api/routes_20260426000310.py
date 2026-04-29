from . import user_api_blueprint
from .. import db, login_manager
from ..models import User
from flask import make_response, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required

from passlib.hash import sha256_crypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Bearer ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())
    response = jsonify(data)
    return response

@user_api_blueprint.route('/api/user/create', methods=['POST'])
def post_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = sha256_crypt.hash(str(request.form['password']))
    username = request.form['username']

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.password = password
    user.authenticated = True

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()})
    return response

@user_api_blueprint.route('/api/user/login', methods=['POST'])
def post_login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user and sha256_crypt.verify(str(request.form['password']), user.password):
        user.encode_api_key()
        db.session.commit()
        login_user(user)
        return make_response(jsonify({'message': 'Logged in successfully', 'api_key': user.api_key}), 200)
    else:
        response = jsonify({'message': 'Invalid username or password'})
        return make_response(response, 401)

@user_api_blueprint.route('/api/user/logout', methods=['POST'])
def post_logout():
    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'Logged out successfully'}), 200)
    return make_response(jsonify({'message': 'No user is currently logged in'}), 400)

@user_api_blueprint.route('/api/user/<username>/exists', methods=['GET'])
def get_username(username):
    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find Username'}), 404
    return response