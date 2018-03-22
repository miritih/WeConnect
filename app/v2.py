from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app.models.v2 import User, Business, Review
from app import create_app, db

# create a version 1 blueprint
version2 = Blueprint('v2', __name__)

# create application istance and push it to app context
app = create_app('development')
app.app_context().push()


@version2.route('auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    username = data['username'].strip().lower()
    if not data or not username or not data["password"]:
        return jsonify({'message': "username or password missing"})
    if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', data['password']):
        return jsonify({
            "Message": """Password must be 6 - 20 Characters\
             and can only contains leters, numbers, and any of !@  # $%"""
        }), 406
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Sorry!! Username taken!"}), 401

    hashed_password = generate_password_hash(data['password'],
                                             method='sha256')
    new_user = User(username=data['username'].strip(),
                    password=hashed_password,
                    first_name=data['first_name'],
                    last_name=data['last_name']
                    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "user created!"}), 201
