from flask import Blueprint, jsonify, request
import os
from utils.json_schema import (login_required, review_schema)
from app.models.v2 import Review, Business
from app import create_app, db
from cerberus import Validator

# create a version 1 blueprint
review = Blueprint('reviews', __name__)

# create application istance and push it to app context
app = create_app(os.getenv('APP_SETTINGS'))
app.app_context().push()


@review.route('businesses/<businessId>/reviews', methods=['POST'])
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
        return jsonify({"message": "Business not found"}), 401
    if biz.bsowner == current_user:
        return jsonify({"Error": "Sorry!, You cannot review your own business"}), 401
    review = Review(title=data['title'], body=data['review'],
                    user_id=current_user.id, business_id=biz.id)
    db.session.add(review)
    db.session.commit()
    return jsonify({
        "message": "Your Review was added",
        "Review": {'id': review.id, 'title': review.title, 'body': review.body,
                   'user_id': review.user_id, 'business_id': review.business_id
                   }}), 201


@review.route('businesses/<businessId>/reviews', methods=['GET'])
def get_business_reviews(businessId):
    """Gets all reviews for a business"""
    business = Business.query.filter_by(id=businessId).first()
    if not business:
        return jsonify({"message": "Business not found"}), 401
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    # get paginated list of businesses. default is page 1
    reviews = Review.query.filter_by(
        business_id=businessId).order_by(Review.created_at.desc()).paginate(
        page, limit, False).items

    if not reviews:
        return jsonify({"message": "No Reviews for this business"})

    return jsonify([{
        'id': review.id, 'title': review.title, 'body': review.body,
        'business_id': review.rvwbusines.id, 'user_id': review.rvwowner.id
    }for review in reviews])


@review.route('businesses/reviews/<reviewId>', methods=['PUT'])
@login_required
def update_business_reviews(current_user, reviewId):
    """This endpoint will update a review only
    the review ownner can update the reviewId"""
    review = Review.query.filter_by(id=reviewId).first()
    if not review:
        return jsonify({"Error": "Review does not exist"})
    if current_user.id != review.user_id:
        return jsonify({"Error": "you can only Update your reviews"})
    data = request.get_json()
    validator = Validator(review_schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return jsonify({"Errors": errors}), 401
    review.title = data['title']
    review.body = data['review']
    db.session.commit()
    return jsonify({
        "message": "Review Updated",
        "Review": {'id': review.id, 'title': review.title, 'body': review.body,
                   'business_id': review.rvwbusines.id, 'user_id': review.rvwowner.id
                   }})
