from flask import Blueprint, jsonify, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
import string
import random
import datetime
from flask_mail import Message
from utils.json_schema import (reg_user_schema, login_schema, reset_pass,
                               update_user_schema, login_required, forgot_pass)
from app.models.v2 import User
from app import create_app, db, mail
from cerberus import Validator

# create a version 1 blueprint
auth = Blueprint('auth', __name__)

# create application istance and push it to app context
app = create_app(os.getenv('APP_SETTINGS'))
app.app_context().push()


@auth.route('auth/register', methods=['POST'])
def register():
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()
    validator = Validator(reg_user_schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    username = data['username'].strip().lower()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=username, email=data['email'],
                    password=hashed_password, first_name=data['first_name'],
                    last_name=data['last_name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "Details": {"first_name": new_user.first_name,
                    "username": new_user.username, "last_name": new_user.last_name,
                    "email": new_user.email},
        "Success": "user created!"}), 201


@auth.route('auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    try:
        auth = request.get_json()
        validator = Validator(login_schema)
        validator.validate(auth)
        errors = validator.errors
        if errors:
            return jsonify({"Errors": errors}), 401
        username = auth['username'].strip().lower()
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, auth['password']):
            user_data = {
                "username": user.username, "email": user.email,
                "last_name": user.last_name, "image": user.image,
                "first_name": user.first_name}
            token = jwt.encode({
                'username': user.username, 'user': user_data,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=120)}, os.getenv("SECRET_KEY"))
            user.logged_in = True
            db.session.commit()
            return jsonify({"auth_token": token.decode('UTF-8')}), 200
        return jsonify({"message": "Wrong password!"}), 401
    except Exception:
        return jsonify({
            "Error": "Error!, check you are sending correct information"}), 400


@auth.route('auth/logout', methods=['POST'])
@login_required
def logout(current_user):
    """method to logout user"""
    current_user.logged_in = False
    db.session.commit()
    return jsonify({"message": "Logged out!"}), 200


@auth.route('auth/reset-password', methods=['PUT'])
@login_required
def reset_password(current_user):
    """Reset password for users"""
    data = request.get_json()
    validator = Validator(reset_pass)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    if check_password_hash(current_user.password, data['old_password']):
        hashed_password = generate_password_hash(
            data['password'].strip(), method='sha256')
        current_user.password = hashed_password
        db.session.commit()
        return jsonify({"message": "password updated"})
    eror = {
        'old_password': "Wrong old Password"
    }
    return jsonify({"Errors": eror}), 406


@auth.route('auth/update-profile', methods=['PUT'])
@login_required
def update_profile(current_user):
    """ Update user profile"""
    data = request.get_json()
    validator = Validator(update_user_schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    current_user.username = data['username']
    current_user.email = data['email'],
    current_user.first_name = data['first_name'],
    current_user.last_name = data['last_name']
    current_user.image = data['image']
    db.session.commit()
    return jsonify({
        "Success": "user updated!",
        "Details": {"email": current_user.email, "username": current_user.username,
                    "first_name": current_user.first_name, "last_name": current_user.last_name
                    }}), 201


@auth.route('auth/forgot-password', methods=['PUT'])
def forgot_password():
    """Sends a new password to a registred email."""
    data = request.get_json()
    validator = Validator(forgot_pass)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 422
    user = User.query.filter_by(email=data['email']).first()
    password = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()
    msg = Message("Password reset",
                  sender="noreply@andela.com",
                  recipients=[user.email])
    link = url_for('auth.login')
    msg.html = render_template('/mails/forgot_password.html',
                               username=user.username, password=password, email=user.email)
    try:
        mail.send(msg)
        return jsonify({"Sucess": "New password sent to your email"})
    except Exception as e:
        return jsonify({"Error": "Opp! an error occured, email was not sent"}), 401
