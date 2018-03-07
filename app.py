from flask import Flask, Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import uuid
import datetime
import os
from models import User, Business, Reviews
from instance.config import app_config

# create a flask app instance

bp = Blueprint('app', __name__)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.register_blueprint(bp)
    return app


# instance of model that will store app data
# application will use data structures to srore data
user_model = User()
business_model = Business()
review_model = Reviews()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message': 'Token is missing, login to get token'}), 401
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            if data['username'] in user_model.user_token:
                current_user = user_model.users[data['username']]
            else:
                return jsonify({"message": "You are not logged in"}), 401
        except:
            return jsonify({'message': 'Token is invalid or Expired!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    try:
        data = request.get_json()  # get data from the api consumer
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        if data['username'] in user_model.users:  # test if username exists
            return jsonify({"message": "Sorry!! Username taken!"})
        data = user_model.add_user(data['username'],
                                   hashed_password,
                                   data['first_name'],
                                   data['last_name']
                                   )
        return jsonify({"message": "user created!"}), 201
    except Exception as e:
        return jsonify({"Error": "Error occured, use correct data format"})


@bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    try:
        auth = request.get_json()
        if not auth or not auth['username'] or not auth['password']:
            return jsonify({"message": "login required!"}), 401
        if auth['username'] not in user_model.users.keys():
            return jsonify({"message": "Username not found!"}), 401
        user = user_model.users[auth['username']]
        if check_password_hash(user['password'], auth['password']):
            token = jwt.encode({
                'username': user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
                os.getenv("SECRET_KEY")
            )
            user_model.user_token[user['username']] = token.decode('UTF-8')
            return jsonify({"auth_token": token.decode('UTF-8')}), 200
        return jsonify({"message": "login required!"}), 401
    except Exception as e:
        return jsonify({"error": "Error occured, use correct data format"})


@bp.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout(current_user):
    """method to logout user"""
    token = None
    if 'access-token' in request.headers:
        try:
            token = request.headers['access-token']
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            if data['username'] in user_model.user_token.keys():
                del user_model.user_token[data['username']]
                return jsonify({"message": "Logged out!"}), 200
        except:
            return jsonify({'message': 'Token is invalid or Expired!'})

    return jsonify({'message': 'Token not passed'}), 401


@bp.route('/api/v1/auth/reset-password', methods=['PUT'])
@login_required
def reset_password(current_user):
    """Reset password for users"""
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        usr = user_model.users[current_user["username"]]
        usr.update({"password": hashed_password})
        return jsonify({"message": "password updated"})
    except Exception as e:
        return jsonify({"message": "error! Check you are sending correct data"})


@bp.route('/api/v1/businesses', methods=['POST'])
@login_required
def register_business(current_user):
    """endpoint to create a new business"""
    data = request.get_json()
    if not data or not data['name']:
        return jsonify({"message": "Name must be available!"}), 401
    for busines in business_model.businesses.values():
        if data['name'] == busines['name']:
            return jsonify({"message": "Sorry!! Name taken!"}), 401
    # update business
    user_id = current_user['username']
    business_model.add_businesses(data['name'], data['location'],
                                  data['category'], data['bio'], user_id)
    return jsonify({"message": "Business created"}), 201


@bp.route('/api/v1/businesses/<businessId>', methods=['PUT'])
@login_required
def update_business(current_user, businessId):
    """ Get business id and update business"""
    try:
        if businessId in business_model.businesses:
            biz = business_model.businesses[businessId]
        data = request.get_json()
        update = {
            'id': uuid.uuid4(),
            'name': data['name'],
            'location': data['location'],
            'category': data['category'],
            "bio": data['bio'],
            'user_id': current_user['username']
        }
        if biz['user_id'] == current_user['username']:
            biz = update
            return jsonify({"message": "business updated!"})
        return jsonify({"message": "Sorry! You can only update your business!!"}), 401
    except Exception as e:
        return jsonify({"message": "error! Check you are sending correct data"}), 401


@bp.route('/api/v1/businesses', methods=['GET'])
@login_required
def get_busineses(current_user):
    """Returns all registered businesses"""
    return jsonify(business_model.businesses)


@bp.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
@login_required
def delete_business(current_user, businessId):
    """ deletes a business"""
    if businessId in business_model.businesses:
        bs = business_model.businesses[businessId]
        if bs['user_id'] == current_user['username']:
            del business_model.businesses[businessId]
            return jsonify({"message": "Business Deleted"}), 201
        return jsonify({"message": "Sorry! You can only delete your business!!"}), 401
    return jsonify({"message": "Business not found"}), 401


@bp.route('/api/v1/businesses/<business_id>', methods=['GET'])
@login_required
def get_business(current_user, business_id):
    """ returns a single business"""
    if business_id in business_model.businesses:
        data = business_model.businesses[business_id]
        return jsonify(data)
    return jsonify({"message": "Business not found"}), 401


@bp.route('/api/v1/businesses/<businessId>/reviews', methods=['POST'])
@login_required
def create_review(current_user, businessId):
    """ Add revies to a business. only logged in users"""
    data = request.get_json()
    if not data or not data['review']:
        return jsonify({"message": "No review in your data"}), 401
    if businessId not in business_model.businesses:
        return jsonify({"message": "Business not found"}), 401
    user_id = current_user['username']
    review_model.add_review(data['review'], user_id, businessId)
    return jsonify({"message": "Your Review was added"}), 201


@bp.route('/api/v1/businesses/<businessId>/reviews', methods=['GET'])
@login_required
def get_business_reviews(current_user, businessId):
    """Gets all reviews for a business"""
    if businessId not in business_model.businesses:
        return jsonify({"message": "Business not found"})
    all_reviews = []
    for review in review_model.reviews.values():
        if review['business_id'] == businessId:
            all_reviews.append(review)
    return jsonify(all_reviews)
    # for review in review_model.reviews:

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
if __name__ == '__main__':
    app.run()
