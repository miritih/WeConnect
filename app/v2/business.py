from flask import Blueprint, jsonify, request
import os
from utils.json_schema import (new_business, business_update, login_required)
from utils.validations import search
from app.models.v2 import Business
from app import create_app, db
from cerberus import Validator

# create a version 1 blueprint
version2 = Blueprint('v2', __name__)

# create application istance and push it to app context
app = create_app(os.getenv('APP_SETTINGS'))
app.app_context().push()


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
        description=data['description'],
        user_id=current_user.id
    )
    db.session.add(new_biz)
    db.session.commit()
    return jsonify({
        "message": "Business created", "Business": {'update_at': new_biz.updated_at,
                                                    "category": new_biz.category, 'description': new_biz.description,
                                                    "name": new_biz.name, "location": new_biz.location,
                                                    'user_id': new_biz.bsowner.id, 'created_at': new_biz.created_at,
                                                    "id": new_biz.id}}), 201


@version2.route('businesses/<business_id>', methods=['GET'])
def get_business(business_id):
    """ returns a single business"""
    business = Business.query.filter_by(id=business_id).first()
    if business:
        return jsonify({'id': business.id, 'user_id': business.bsowner.id,
                        'created_at': business.created_at, 'name': business.name,
                        'location': business.location, 'description': business.description,
                        'category': business.category, 'update_at': business.updated_at
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
        "Results": [{'category': business.category, 'created_at': business.created_at,
                     'name': business.name, 'location': business.location,
                     'id': business.id, 'category': business.category,
                     'description': business.description, 'user_id': business.bsowner.id,
                     'update_at': business.updated_at
                     } for business in all],
        "per_page": results.per_page, "page": results.page,
        "total_pages": results.pages, "total_results": results.total
    })


@version2.route('businesses', methods=['GET'])
def get_busineses():
    """Returns all registered businesses"""
    # set all serch parameters.
    vars = {
        'page': request.args.get('page', 1, type=int),
        'name': request.args.get('q', None, type=str),
        'location': request.args.get('location', default=None, type=str),
        'category': request.args.get('category', None, type=str),
        'limit': request.args.get('limit', 10, type=int)
    }
    # get paginated list of businesses.
    results = search(vars)
    all = results.items
    return jsonify({
        "page": results.page,
        "total_results": results.total,
        "total_pages": results.pages,
        "per_page": results.per_page,
        "objects": [{'id': business.id, 'name': business.name,
                     'user_id': business.bsowner.id, 'created_at': business.created_at,
                     'location': business.location, 'category': business.category,
                     'description': business.description, 'update_at': business.updated_at
                     } for business in all
                    ]})


@version2.route('businesses/search', methods=['GET'])
def search_busineses():
    """search for business using name location or category"""
    # set all serch parameters.
    search_vars = {
        'name': request.args.get('q', None, type=str),
        'location': request.args.get('location', default=None, type=str),
        'category': request.args.get('category', None, type=str),
        'page': request.args.get('page', 1, type=int),
        'limit': request.args.get('limit', 10, type=int)
    }
    # get paginated list of businesses.
    results = search(search_vars)
    all_paginated = results.items
    return jsonify({
        "total_results": results.total,
        "total_pages": results.pages,
        "page": results.page,
        "per_page": results.per_page,
        "businesses": [{'id': business.id, 'name': business.name,
                        'user_id': business.bsowner.id, 'created_at': business.created_at,
                        'location': business.location, 'category': business.category,
                        'description': business.description, 'update_at': business.updated_at
                        } for business in all_paginated]})


@version2.route('businesses/<businessId>', methods=['PUT'])
@login_required
def update_business(current_user, businessId):
    """ Get business id and update business"""
    business = Business.query.filter_by(id=businessId).first()
    if not business:
        return jsonify({"message": "Business not found"})
    data = request.get_json()
    duplicate = Business.query.filter(
        Business.name.ilike(data['name'])).first()
    validator = Validator(business_update)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    if duplicate and duplicate.name != business.name:
        return jsonify({"Error": "Business name taken"})
    if business.bsowner.id == current_user.id:
        business.location = data['location']
        business.category = data['category']
        business.name = data['name']
        business.description = data['description']
        db.session.commit()
        return jsonify({
            "message": "business updated!",
            "Details": {
                "name": business.name, "location": business.location,
                "category": business.category
            }}), 202
    return jsonify({"message": "Sorry! You can only update your business!!"}), 401


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
