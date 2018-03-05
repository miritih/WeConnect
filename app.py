from flask import Flask, jsonify, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from models import User
from instance.config import app_config

# create a flask app instance


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    return app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

# instance of model taht will store app data
# application will use data structures to srore data
user_model = User()


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    hashed_password = generate_password_hash(data['password'], method='sha256')
    if data['username'] in user_model.get_all_users():  # test if username exists
        return jsonify({"message": "Sorry!! Username taken!"})
    user_model.add_user(data['username'], hashed_password,
                        data['first_name'], data['last_name'])
    return jsonify({'message': 'User created!'}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"message": "login required!"}), 401
    if auth['username'] in user_model.get_all_users():
        user = user_model.get_all_users()[auth['username']]
    else:
        return jsonify({"message": "Username not found!"}), 401
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode(
            {'username': user['username']}, app.config['SECRET_KEY'])
        session['username'] = user['username']
        session['token'] = token
        return jsonify({"token": token.decode('UTF-8')}), 200
    return jsonify({"message": "login required!"}), 401


if __name__ == '__main__':
    app.run()
