"""
This files stores all validation schema for all POST and PUT json data
It's what will be used  to validate user data
"""

from flask import Blueprint, jsonify, request   
from utils.validations import (validate_field,
                                  validate_email,
                                  username_taken,
                                  validate_password,
                                  forgot_password,
                                  )
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import jwt
import datetime
from app.models.v2 import User

# register user schema. will validate new user data
reg_user_schema = {
    'username': {
        'type': 'string',
        'required': True,
        'validator': validate_field
    },
    'email': {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_email
    },
    'password': {
        'type': 'string',
        'validator': validate_password,
        'required': True,
        'empty': False,
    },
    'first_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'last_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    }
}
#update user schema
update_user_schema = {
    'username': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'email': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'first_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'last_name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'image': {
        'type': 'string',
        'required': True,
        'empty': False,
    }
}
# login data schema. will validate login data
login_schema = {
    "username": {
        'type': 'string',
        'required': True,
        'validator': username_taken
    },
    "password": {
        'type': 'string',
        'required': True
    }
}
# reset-password data schema

reset_pass = {
    "password": {
        'type': 'string',
        'validator': validate_password,
        'required': True
    },
    "old_password": {
        'type': 'string',
        'required': True
    }
}

new_business = {
    "name": {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': validate_field
    },
    "location": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "category": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "description": {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
business_update = {
    "name": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "location": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "category": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "description": {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
review_schema = {
    "review": {
        'type': 'string',
        'required': True,
        'empty': False
    },
    "title": {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
forgot_pass ={
    'email': {
        'type': 'string',
        'required': True,
        'empty': False,
        'validator': forgot_password
    },
}
def login_required(f):
    """
    login decorator function
    it checks the authentication token verify if its valid,
    then return the aunthenticated user
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' not in request.headers:
            return jsonify({
                'message': 'Token is missing, login to get token'
            }), 401
        try:
            token = request.headers['access-token']
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            current_user = User.query.filter_by(
                username=data['username'],
                logged_in=True
            ).first()
            if not current_user:
                return jsonify({"message": "You are not logged in"}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid or Expired!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated