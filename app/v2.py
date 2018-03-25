from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import re
from instance.json_schema import reg_user_schema
from app.models.v2 import User, Business, Review
from app import create_app, db
from cerberus import Validator

# create a version 1 blueprint
version2 = Blueprint('v2', __name__)

# create application istance and push it to app context
app = create_app('development')
app.app_context().push()


@version2.route('auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()
    validator = Validator(reg_user_schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        if 'password' in errors.keys():
            errors['password'] = "Password must be 6 - 20 Characters and can only contains leters, numbers, and any of !@  # $%"
        return jsonify(errors), 401

    username = data['username'].strip().lower()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=username,
                    email=data['email'],
                    password=hashed_password,
                    first_name=data['first_name'],
                    last_name=data['last_name']
                    )
    db.session.add(new_user)
    a = db.session.commit()
    print(new_user)
    return jsonify({
        "Success": "user created!",
        "Details": {
            "email": new_user.email,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }), 201
