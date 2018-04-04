from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re
import os
import jwt
import datetime
from instance.json_schema import (reg_user_schema,
                                  login_schema,
                                  reset_pass,
                                  new_business,
                                  review_schema,
                                  )
from instance.validations import search
from app.models.v2 import User, Business, Review
from app import create_app, db
from cerberus import Validator

# create a version 1 blueprint
version2 = Blueprint('v2', __name__)

# create application istance and push it to app context
app = create_app('development')
app.app_context().push()


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


@version2.route('auth/register', methods=['POST'])
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
    new_user = User(username=username,
                    email=data['email'],
                    password=hashed_password,
                    first_name=data['first_name'],
                    last_name=data['last_name']
                    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "Success": "user created!",
        "Details": {
            "email": new_user.email,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }), 201


@version2.route('auth/login', methods=['POST'])
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
            token = jwt.encode({
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)},
                os.getenv("SECRET_KEY")
            )
            user.logged_in = True
            db.session.commit()
            return jsonify({"auth_token": token.decode('UTF-8')}), 200
        return jsonify({"message": "Wrong password!"}), 401
    except Exception as e:
        return jsonify({
            "Error": "Error!, check you are sending correct information"}), 400


@version2.route('auth/logout', methods=['POST'])
@login_required
def logout(current_user):
    """method to logout user"""
    current_user.logged_in = False
    db.session.commit()
    return jsonify({"message": "Logged out!"}), 200


@version2.route('auth/reset-password', methods=['PUT'])
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
    return jsonify({"message": "Wrong old Password"}), 406


@version2.route('businesses', methods=['POST'])
@login_required
def register_business(current_user):
    """endpoint to create a new business"""
    data = request.get_json()
    validator = Validator(new_business)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    # Create business
    new_biz = Business(
        name=data['name'].strip().lower(),
        location=data['location'],
        category=data['category'],
        bio=data['bio'],
        user_id=current_user.id
    )
    db.session.add(new_biz)
    db.session.commit()
    return jsonify({
        "message": "Business created", "Business": {
            "id": new_biz.id,
            "name": new_biz.name,
            "location": new_biz.location,
            "category": new_biz.category,
            'bio': new_biz.bio,
            'user_id': new_biz.bsowner.id,
            'created_at': new_biz.created_at,
            'update_at': new_biz.updated_at
        }
    }), 201


@version2.route('businesses/<business_id>', methods=['GET'])
def get_business(business_id):
    """ returns a single business"""
    business = Business.query.filter_by(id=business_id).first()
    if business:
        return jsonify({
            'id': business.id,
            'name': business.name,
            'location': business.location,
            'category': business.category,
            'bio': business.bio,
            'user_id': business.bsowner.id,
            'created_at': business.created_at,
            'update_at': business.updated_at
        })
    return jsonify({"message": "Business not found"}), 401


@version2.route('businesses/user', methods=['GET'])
@login_required
def get_user_businesses(current_user):
    """ returns all user businesses"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    results = Business.query.filter_by(user_id=current_user.id).paginate(
        page, limit, True)
    all = results.items
    return jsonify({
        "total_results": results.total,
        "total_pages": results.pages,
        "page": results.page,
        "per_page": results.per_page,
        "objects":
        [{
            'id': business.id,
            'name': business.name,
            'location': business.location,
            'category': business.category,
            'bio': business.bio,
            'user_id': business.bsowner.id,
            'created_at': business.created_at,
            'update_at': business.updated_at
        } for business in all
        ]})


@version2.route('businesses', methods=['GET'])
def get_busineses():
    """Returns all registered businesses"""

   # set all serch parameters.
    vars = {
        'page': request.args.get('page', 1, type=int),
        'limit': request.args.get('limit', 10, type=int),
        'location': request.args.get('location', default=None, type=str),
        'category': request.args.get('category', None, type=str),
        'name': request.args.get('name', None, type=str)
    }

    # get paginated list of businesses. default is page 1
    alll = search(vars)
    print(alll.items)
    results = Business.query.order_by(Business.created_at.desc()).paginate(
        vars['page'], vars['limit'], True)
    all = results.items
    return jsonify({
        "total_results": results.total,
        "total_pages": results.pages,
        "page": results.page,
        "per_page": results.per_page,
        "objects":
        [{
            'id': business.id,
            'name': business.name,
            'location': business.location,
            'category': business.category,
            'bio': business.bio,
            'user_id': business.bsowner.id,
            'created_at': business.created_at,
            'update_at': business.updated_at
        } for business in all
        ]})


@version2.route('businesses/<businessId>', methods=['PUT'])
@login_required
def update_business(current_user, businessId):
    """ Get business id and update business"""

    biz = Business.query.filter_by(id=businessId).first()
    if not biz:
        return jsonify({"message": "Business not found"})
    data = request.get_json()
    if data['name'] != biz.name:
        if Business.query.filter_by(name=data['name']).first():
            return jsonify({"Error": "Sorry!! Business name taken!"})
    if biz.bsowner.id == current_user.id:
        biz.location = data['location'] if data[
            'location'] else biz.location
        biz.category = data['category'] if data[
            'category'] else biz.category
        biz.name = data['name'] if data['name'] else biz.name
        biz.bio = data['bio'] if data['bio'] else biz.bio
        db.session.commit()
        return jsonify({
            "message": "business updated!",
            "Details": {
                "name": biz.name,
                "location": biz.location,
                "category": biz.category,
            }
        }), 202

    return jsonify({
        "message": "Sorry! You can only update your business!!"
    }), 401


@version2.route('businesses/<businessId>', methods=['DELETE'])
@login_required
def delete_business(current_user, businessId):
    """ deletes a business"""
    business = Business.query.filter_by(id=businessId).first()
    if business:
        if business.bsowner.id == current_user.id:
            db.session.delete(business)
            db.session.commit()
            return jsonify({
                "message": "Business Deleted",
            }), 201
        return jsonify({
            "message": "Sorry! You can only delete your business!!"
        }), 401
    return jsonify({"message": "Business not found"}), 401


@version2.route('businesses/<businessId>/reviews', methods=['POST'])
@login_required
def create_review(current_user, businessId):
    """ Add revies to a business. only logged in users"""
    data = request.get_json()
    validator = Validator(review_schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    biz = Business.query.filter_by(id=businessId).first()
    if not biz:
        return jsonify({
            "message": "Business not found"
        }), 401
    review = Review(
        title=data['title'],
        body=data['review'],
        user_id=current_user.id,
        business_id=biz.id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({
        "message": "Your Review was added",
        "Review": {
            'id': review.id,
            'title': review.title,
            'body': review.body,
            'user_id': review.user_id,
            'business_id': review.business_id
        }
    }), 201


@version2.route('businesses/<businessId>/reviews', methods=['GET'])
def get_business_reviews(businessId):
    """Gets all reviews for a business"""
    business = Business.query.filter_by(id=businessId).first()
    if not business:
        return jsonify({
            "message": "Business not found"
        }), 401
    page = request.args.get('page', 1, type=int)
    # get paginated list of businesses. default is page 1
    reviews = Review.query.filter_by(business_id=businessId).order_by(Review.created_at.desc()).paginate(
        page, 5, False).items

    if not reviews:
        return jsonify({"message": "No Reviews for this business"})

    return jsonify([{
        'id': review.id,
        'title': review.title,
        'body': review.body,
        'business_id': review.rvwbusines.id,
        'user_id': review.rvwowner.id
    }for review in reviews
    ])


@version2.route('businesses/<businessId>/reviews/<reviewId>', methods=['DELETE'])
@login_required
def delete_business_reviews(current_user, businessId, reviewId):
    """Delete a business review"""
    review = Review.query.filter_by(id=reviewId).first()
    if not review:
        return jsonify({"Error": "Review does not exist"})
    if current_user.id != review.user_id:
        return jsonify({"Error": "you can only delete your reviews"})
    biz = Business.query.filter_by(id=businessId).first()
    if not biz:
        return jsonify({
            "message": "Business not found"
        }), 401

    db.session.delete(review)
    db.session.commit()
    return jsonify({"sucess": "Review deleted successfully"})


@version2.route('businesses/<businessId>/reviews/<reviewId>', methods=['PUT'])
@login_required
def update_business_reviews(current_user, businessId, reviewId):
    """
    This endpoint will update a review
    only the review ownner can update the reviewId
    """
    review = Review.query.filter_by(id=reviewId).first()
    if not review:
        return jsonify({"Error": "Review does not exist"})
    if current_user.id != review.user_id:
        return jsonify({"Error": "you can only Update your reviews"})
    data = request.get_json()
    biz = Business.query.filter_by(id=businessId).first()
    if not biz:
        return jsonify({
            "message": "Business not found"
        }), 401

    review.title = data['title'] if data['title'] else review.title
    review.body = data['review'] if data['review'] else review.title
    db.session.commit()
    return jsonify({
        "message": "Review Updated",
        "Review": {
            'id': review.id,
            'title': review.title,
            'body': review.body,
            'business_id': review.rvwbusines.id,
            'user_id': review.rvwowner.id
        }
    })
