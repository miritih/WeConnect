from flask import Flask, Blueprint, jsonify, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import uuid
import datetime
import os
from models import User, Business
from instance.config import app_config

# create a flask app instance

bp = Blueprint('app', __name__)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(bp)
    return app


# instance of model that will store app data
# application will use data structures to srore data
user_model = User()
business_model = Business()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing, login to get token'}), 401
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            if data['username'] in user_model.user_token:
                current_user = user_model.users[data['username']]
            else:
                return jsonify({"message": "Token Expired"})
        except:
            return jsonify({'message': 'Token is invalid/Expired!. login to get another'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    hashed_password = generate_password_hash(data['password'], method='sha256')
    if data['username'] in user_model.users:  # test if username exists
        return jsonify({"message": "Sorry!! Username taken!"})
    data = user_model.add_user(data['username'],
                               hashed_password,
                               data['first_name'],
                               data['last_name']
                               )
    return jsonify({"message": "user created!"}), 201


@bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"message": "login required!"}), 401
    if auth['username'] not in user_model.users.keys():
        print(auth['username'] in user_model.users.keys())
        print(user_model.users.keys())
        return jsonify({"message": "Username not found!"}), 401
    user = user_model.users[auth['username']]
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
            os.getenv("SECRET_KEY")
        )
        user_model.user_token[user['username']] = token
        return jsonify({"auth_token": token.decode('UTF-8')}), 200
    return jsonify({"message": "login required!"}), 401


@bp.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    """method to logout user"""
    token = None
    if 'x-access-token' in request.headers:
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            if data['username'] in user_model.user_token:
                del user_model.user_token[data['username']]
                return jsonify({"message": "Logged out!"}), 200
        except:
            return jsonify({'message': 'Token is invalid/Expired!. login to get another'})
    if not token:
        return jsonify({'message': 'Not logged in or no Token passed'}), 401


@bp.route('/api/v1/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """Reset password for users"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    usr = user_model.users[current_user["username"]]
    usr.update({"password": hashed_password})
    return jsonify({"message": "password updated"})


@bp.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """endpoint to create a new business"""
    data = request.get_json()
    if not data or not data['name']:
        return jsonify({"message": "Name must be available!"}), 402

    if data['name'] in business_model.businesses:
        return jsonify({"message": "Sorry!! Name taken!"}), 402
    # add business
    user_id = current_user['username']
    business_model.add_businesses(data['name'], data['location'],
                                  data['category'], data['bio'], user_id)
    return jsonify({"message": "Business created"}), 201


@bp.route('/api/v1/businesses/<businessId>', methods=['POST'])
@token_required
def update_business(current_user, businessId):
    """ Get business id and update business"""
    data = request.get_json()
    update = {
        'id': uuid.uuid4(),
        'name': data['name'],
        'location': data['location'],
        'category': data['category'],
        "bio": data['bio'],
        'user_id': current_user['username']
    }
    business_model.businesses[businessId] = update
    return jsonify({"message": "business updated!"})


@bp.route('/api/v1/businesses', methods=['GET'])
def get_busineses():
    """Returns all registered businesses"""
    return jsonify(business_model.businesses)


config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
if __name__ == '__main__':
    app.run()
